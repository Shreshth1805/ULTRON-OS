from collections import deque

from app.execution.task import Task


class TaskQueue:

    def __init__(self):

        self.queue = deque()

    def push(
        self,
        task: Task
    ):

        self.queue.append(task)

    def pop(self):

        if self.queue:

            return self.queue.popleft()

        return None

    def empty(self):

        return len(self.queue) == 0

    def size(self):

        return len(self.queue)


task_queue = TaskQueue()