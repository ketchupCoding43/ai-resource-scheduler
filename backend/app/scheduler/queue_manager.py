from queue import Queue

request_queue = Queue()


def enqueue(item):
    request_queue.put(item)


def dequeue():
    if request_queue.empty():
        return None

    return request_queue.get()


def queue_size():
    return request_queue.qsize()