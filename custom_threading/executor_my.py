import concurrent.futures
import logging

from custom_threading.long_task import LongTask


class MyExecutor(object):
    _executor = concurrent.futures.ThreadPoolExecutor(max_workers=500)

    def __init__(self, thread_count, task):
        self._thread_count = thread_count
        self._task = LongTask(task)
        self.logger = logging.getLogger(__name__)
        pass

    def start(self):
        self.logger.debug("Launching with thread count: " + str(self._thread_count))

        futures = []
        for i in range(0, self._thread_count):
            self.logger.debug("Submitting task #" + str(i))
            futures.append(self._executor.submit(self._task.run_task))

        return futures

    def stop(self):
        self._task.stop_task()
        self._executor.shutdown()
        print("task stopped")
        return

    # not working. waits forever for tasks to finish
    def shutdown_executor(self, wait=False):
        self._executor.shutdown(wait=wait)
        print("executor is down")
        return
