import time
import threading


class ThreadManager:
    def __init__(self, task_queue) -> None:
        self.task_queue = task_queue

    def __initialize_threads(self, task_queue) -> None:
        for item in task_queue:
            thread = threading.Thread(
                target=item,
                daemon=True
            )
            thread.start()

    def start_tasks(self) -> None:
        threading.Thread(
            target=self.__initialize_threads,
            daemon=True,
            args=[self.task_queue]
        ).start()

        try:
            print("Bot is Running...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("")
