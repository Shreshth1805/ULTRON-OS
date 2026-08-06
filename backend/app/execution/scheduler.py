from app.execution.queue import task_queue


class Scheduler:

    def add_tasks(
        self,
        tasks
    ):

        for task in tasks:

            task_queue.push(task)

    def next_task(self):

        return task_queue.pop()


scheduler = Scheduler()