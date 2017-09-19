class LongTask(object):
    _is_running = False

    def __init__(self, task):
        self._task = task

    def run_task(self):
        self._is_running = True
        while self._is_running:
            result = self._task()
            if result is "stop":
                print("received stop signal")
                self._is_running = False

        return

    def stop_task(self):
        self._is_running = False
        return
