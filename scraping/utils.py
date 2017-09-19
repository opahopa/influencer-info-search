import os, time, logging
import random
from random import randint


class Utils(object):
    _browser_agents_file = os.path.join('scraping', 'user-agents.txt')
    _browser_agents_list = []

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @classmethod
    def get_random_browser_agent(cls):
        if len(cls._browser_agents_list) < 1:
            cls._browser_agents_list = list(filter(None, (line.rstrip() for line in open(cls._browser_agents_file))))

        return random.choice(cls._browser_agents_list)

    @classmethod
    def random_sleep(self):
        sleep_time = randint(5, 15)
        print("Random sleep: %s sec." % sleep_time)
        time.sleep(sleep_time)
