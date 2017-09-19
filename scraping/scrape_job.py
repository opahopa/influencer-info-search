import logging
import threading
import sys, traceback
import string
import re

import requests
import utils

from scraping.data_singleton import DataSingleton
from scraping.scraping import ScrapeFactory
from scraping.models import Proxy

import os


class InfoScraper:
    lock = threading.Lock()
    _connection_timeout = 15
    is_use_proxy = True

    proxy_filename = "proxy_list.txt"
    names_filename = "names_list.txt"

    dataCache = DataSingleton()
    dataCache.results_list = []

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        try:
            # print("size "+str(os.path.getsize(self.proxy_filename)))
            # print("proxy life lines: ", utils.file_len(self.proxy_filename))

            if os.path.getsize(self.proxy_filename) and utils.file_len(self.proxy_filename) > 0:
                self._proxy_list_file = list(filter(None, (line.rstrip() for line in open(self.proxy_filename))))
            else:
                self.is_use_proxy = False

            self.dataCache.names_list = []

            if os.path.getsize(self.names_filename) and utils.file_len(self.names_filename) > 0:
                self.dataCache.names_list = list(
                    filter(None, (line.rstrip() for line in open(self.names_filename, encoding="utf8"))))
            else:
                self.logger.error("Please input a names list.")

            self.logger = logging.getLogger(__name__)
        except IOError:
            print("proxy/name file I/O error")

        pass

    def _get_proxy_from_list_and_check(self):
        with self.lock:
            if self._proxy_list_file.__len__() == 0:
                self._proxy_list_file = list(filter(None, (line.rstrip() for line in open(self.proxy_filename))))

            _proxy = str(self._proxy_list_file[0])
            del self._proxy_list_file[0]

        if self._check_single_proxy(_proxy) is not True:
            self._get_proxy_from_list_and_check()

        self.logger.debug("using proxy: %s" % _proxy)
        return _proxy

    def _check_single_proxy(self, proxy_string):
        proxies = {'http': 'http://' + proxy_string}

        self.logger.debug("Checking proxy :: %s" % proxy_string)
        try:
            json_response = requests.get('http://freegeoip.net/json/', proxies=proxies,
                                         timeout=self._connection_timeout)

            if json_response.status_code == 200:
                self.logger.debug("Proxy check status code 200")
                return True
            else:
                self.logger.debug(
                    "Proxy check: %s " % proxy_string + "invalid status code: %s " % str(json_response.status_code))
                return False

        except requests.exceptions.RequestException:
            print("proxy : %s, is invalid " % proxy_string)
            return False

    def scrape_main(self):
        """
        :return: False if proxy is invalid :: True if proxy checked and result saved
        """

        # reload proxy if they done
        _current_proxy = None
        if self.is_use_proxy is True:
            try:
                _current_proxy = Proxy(self._get_proxy_from_list_and_check(), 'http')
                if _current_proxy is None:
                    return "stop"
            except IndexError:
                return "stop"

        # _current_proxy = Proxy("127.0.0.1:8888", 'http')
        scrape_factory = ScrapeFactory(proxy=_current_proxy)

        name = ''
        try:
            self.logger.debug('names list length: %s' % len(self.dataCache.names_list))
            if len(self.dataCache.names_list) == 0:
                return "stop"

            with self.lock:
                name = self.dataCache.names_list[0]
                name = re.sub(r'['+string.punctuation+']', " ", name, flags=re.IGNORECASE)
                del self.dataCache.names_list[0]

            result = scrape_factory.run_info_search(name)
            if result is not None:
                self.dataCache.results_list.append(result)

        except Exception:
            print(traceback.format_exc())
            self.logger.debug("Adding the name back: %s" % name)
            return True
