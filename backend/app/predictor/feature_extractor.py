import re

TECHNICAL_DOMAINS = {
    "kubernetes": 30,
    "docker": 20,
    "kafka": 25,
    "terraform": 25,
    "ansible": 20,
    "machine learning": 30,
    "deep learning": 35,
    "neural network": 35,
    "distributed systems": 35,
    "service mesh": 30,
    "istio": 30,
    "gpu": 15,
    "cuda": 30,
    "database": 15,
    "sql": 15,
    "compiler": 25,
    "operating system": 20,
    "linux": 15,
    "windows": 10,
    "chatgpt": 20,
    "transformer": 25,
}

COMPLEXITY_TERMS = {
    "detail": 15,
    "detailed": 15,
    "architecture": 20,
    "internals": 20,
    "implementation": 20,
    "design": 15,
    "compare": 15,
    "analysis": 15,
    "advanced": 20,
    "working": 10,
}

TECHNICAL_KEYWORDS = [
    "linux",
    "docker",
    "kubernetes",
    "network",
    "networking",
    "rbac",
    "cni",
    "csi",
    "service mesh",
    "api",
    "database",
    "machine learning",
    "gpu",
    "distributed",
    "microservice",
    "container",
    "transformer",
    "architecture",
    "workflow",
    "pipeline",
]

CODE_KEYWORDS = [
    "python",
    "java",
    "c++",
    "function",
    "class",
    "object",
    "loop",
    "array",
    "json",
    "yaml",
    "sql",
    "algorithm",
    "program",
    "code",
    "script",
    "implement",
    "develop",
    "build",
]

INTENT_RULES = {
    "DEFINE": ["what is", "define", "meaning of"],
    "EXPLAIN": ["explain", "describe", "working of", "how does"],
    "COMPARE": ["difference", "compare", "versus", "vs"],
    "ARCHITECTURE": ["architecture", "design", "workflow", "pipeline", "internal", "mechanism"],
    "CODE_GENERATION": ["write code", "generate code", "create application", "implement", "develop", "build project"],
    "DEBUGGING": ["error", "exception", "bug", "traceback", "fix"],
    "TUTORIAL": ["step by step", "guide", "walkthrough", "tutorial"],
    "ANALYSIS": ["analyze", "evaluate", "benchmark", "performance"],
}

INTENT_ORDER = [
    "DEFINE",
    "EXPLAIN",
    "COMPARE",
    "ARCHITECTURE",
    "CODE_GENERATION",
    "DEBUGGING",
    "TUTORIAL",
    "ANALYSIS",
]

RESPONSE_SIZE_MAP = {
    "DEFINE": "SMALL",
    "EXPLAIN": "MEDIUM",
    "COMPARE": "MEDIUM",
    "ARCHITECTURE": "LARGE",
    "CODE_GENERATION": "LARGE",
    "DEBUGGING": "MEDIUM",
    "TUTORIAL": "LARGE",
    "ANALYSIS": "LARGE",
    "GENERAL": "MEDIUM",
}

DEFAULT_INTENT = "GENERAL"


def _count_occurrences(text: str, keywords: list[str]) -> int:
    lowered = text.lower()
    return sum(lowered.count(keyword) for keyword in keywords)


def detect_intent(prompt: str) -> str:
    prompt = (prompt or "").lower()

    for intent in INTENT_ORDER:
        if any(keyword in prompt for keyword in INTENT_RULES[intent]):
            return intent

    return DEFAULT_INTENT


def estimate_response_size(prompt: str) -> str:
    intent = detect_intent(prompt)
    return RESPONSE_SIZE_MAP.get(intent, "MEDIUM")


def _topic_count(prompt: str) -> int:
    lowered = (prompt or "").lower()
    topic_signals = set()

    for keyword in TECHNICAL_KEYWORDS + CODE_KEYWORDS:
        if keyword in lowered:
            topic_signals.add(keyword)

    for keyword_list in INTENT_RULES.values():
        for keyword in keyword_list:
            if keyword in lowered:
                topic_signals.add(keyword)

    words = re.findall(r"[a-zA-Z0-9\+\#]+", lowered)
    for word in words:
        if len(word) > 7:
            topic_signals.add(word)

    return len(topic_signals)


def _match_weighted_terms(prompt: str, term_map: dict[str, int]) -> tuple[int, list[str]]:
    lowered = (prompt or "").lower()
    total = 0
    matches = []

    for term, weight in term_map.items():
        if term in lowered:
            total += weight
            matches.append(term)

    return total, matches


def compute_complexity_score(features: dict) -> float:
    intent = features.get("intent", DEFAULT_INTENT)
    expected_response_size = features.get("expected_response_size", "MEDIUM")
    technical_keyword_count = features.get("technical_keyword_count", 0)
    topic_count = features.get("topic_count", 0)

    score = 0.0
    score += technical_keyword_count * 3
    score += topic_count * 5
    score += features.get("semantic_score", 0) * 0.35

    intent_weights = {
        "EXPLAIN": 15,
        "ARCHITECTURE": 30,
        "CODE_GENERATION": 35,
        "DEBUGGING": 25,
        "TUTORIAL": 30,
        "ANALYSIS": 25,
    }
    score += intent_weights.get(intent, 0)

    response_size_weights = {
        "SMALL": 0,
        "MEDIUM": 10,
        "LARGE": 20,
    }
    score += response_size_weights.get(expected_response_size, 10)

    if features.get("code_keyword_count", 0) > 0:
        score += min(15, features["code_keyword_count"] * 2)

    if features.get("comparison_keyword_count", 0) > 0:
        score += 4

    if features.get("question_count", 0) > 1:
        score += 3

    return round(score, 2)


def extract_features(prompt: str):
    prompt = prompt or ""
    lowered = prompt.lower()
    words = re.findall(r"\b\S+\b", prompt)
    sentences = [s for s in re.split(r"[.!?]+", prompt) if s.strip()]

    technical_keyword_count = _count_occurrences(lowered, TECHNICAL_KEYWORDS)
    code_keyword_count = _count_occurrences(lowered, CODE_KEYWORDS)
    comparison_keyword_count = _count_occurrences(lowered, ["difference", "compare", "versus", "vs"])
    explanation_keyword_count = _count_occurrences(lowered, ["explain", "describe", "what is", "how does"])
    step_by_step_keyword_count = _count_occurrences(lowered, ["step", "tutorial", "guide", "implementation", "walkthrough"])
    technical_domain_score, technical_domain_matches = _match_weighted_terms(prompt, TECHNICAL_DOMAINS)
    complexity_term_score, complexity_term_matches = _match_weighted_terms(prompt, COMPLEXITY_TERMS)

    semantic_score = (
        technical_domain_score
        + complexity_term_score
        + explanation_keyword_count * 4
        + step_by_step_keyword_count * 5
        + comparison_keyword_count * 4
    )

    features = {
        "prompt_length": len(prompt),
        "word_count": len(words),
        "sentence_count": len(sentences) or 1,
        "question_count": prompt.count("?"),
        "technical_keyword_count": technical_keyword_count,
        "code_keyword_count": code_keyword_count,
        "comparison_keyword_count": comparison_keyword_count,
        "explanation_keyword_count": explanation_keyword_count,
        "step_by_step_keyword_count": step_by_step_keyword_count,
        "topic_count": _topic_count(prompt),
        "technical_domain_score": technical_domain_score,
        "technical_domain_matches": technical_domain_matches,
        "complexity_term_score": complexity_term_score,
        "complexity_term_matches": complexity_term_matches,
        "semantic_score": semantic_score,
    }

    features["intent"] = detect_intent(prompt)
    features["expected_response_size"] = estimate_response_size(prompt)
    features["complexity_score"] = compute_complexity_score(features)

    return features
