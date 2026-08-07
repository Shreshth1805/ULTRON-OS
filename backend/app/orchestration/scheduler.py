from dataclasses import dataclass, field
import heapq
import time
@dataclass(order=True)
class ScheduledTask:
    # Fields without defaults MUST come first
    priority: int
    task: object = field(compare=False)
    # Fields with defaults come after non-default fields
    created_at: float = field(
        default_factory=time.time,
        compare=True
    )
    retries: int = field(
        default=0,
        compare=False
    )
class TaskScheduler:
    def __init__(self):
        self.queue = []
    # ============================================
    # Add Task
    # ============================================
    def add(
        self,
        task,
        priority: int = 100
    ):
        heapq.heappush(
            self.queue,
            ScheduledTask(
                priority=priority,
                task=task
            )
        )
    # ============================================
    # Get Next Task
    # ============================================
    def next(self):
        if not self.queue:
            return None
        return heapq.heappop(
            self.queue
        ).task
    # ============================================
    # Retry Task
    # ============================================
    def retry(
        self,
        task,
        retries,
        priority=50
    ):
        heapq.heappush(
            self.queue,
            ScheduledTask(
                priority=priority,
                task=task,
                retries=retries
            )
        )
    # ============================================
    # Status
    # ============================================
    def size(self):
        return len(self.queue)
    def empty(self):
        return len(self.queue) == 0
    def clear(self):
        self.queue.clear()
task_scheduler = TaskScheduler()