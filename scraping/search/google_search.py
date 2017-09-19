import traceback
import logging
import requests
import re

from scraping.utils import Utils
from bs4 import BeautifulSoup


class GoogleSearch(object):
    _pages_counter = 0
    _pages_limit = 3
    _results_limit = 30
    request_timeout = 15

    def __init__(self, proxy=None):
        self.logger = logging.getLogger(__name__)
        self.urls_list = []

        try:
            self._s = requests.Session()

            if proxy is not None:
                self._s.proxies = proxy.dict_for_requests()

            self._user_agent_string = Utils.get_random_browser_agent()

        except Exception:
            print(traceback.format_exc())

    def __exit__(self, exc_type, exc_value, traceback):
        self.urls_list = None
        self._pages_counter = 0

    def get_url(self, url, name):
        if url is None:
            url = "https://www.google.com/search?q={0}&oq={0}&sourceid=chrome&ie=UTF-8".format(name)
        else:
            if '&start' in url:
                url = re.sub(r"&start=[0-9]+", '&start=%s' % (self._pages_counter * 10), url)
            else:
                url += '&start=%s' % (self._pages_counter * 10)

        self.logger.info('Parsing url: ' + url)
        return url

    def search(self, name, url=None):
        if self._pages_counter < self._pages_limit and len(self.urls_list) < self._results_limit:
            url = self.get_url(url, name)
        else:
            return self.urls_list

        try:
            r = self._s.get(url, verify=False, timeout=self.request_timeout)

            soup = BeautifulSoup(r.text, 'lxml')
            # print(soup.prettify())

            if self._check_empty_google_results(soup) is "done":
                return

            results_list = soup.find_all('div', class_="g")
            print('Google results count: %s' % len(results_list))
            for index, result in enumerate(results_list):
                try:
                    if 'document.querySelector' not in result.__str__():
                        site_url = result.h3.a['href'].lstrip("/url?q=")
                        site_title = result.h3.a.text
                        self.urls_list.append({'position': (index + 1) + (self._pages_counter * 10), 'url': site_url,
                                               'title': site_title})
                except:
                    pass

            self.logger.info("Going to next page")
            self._pages_counter += 1
            Utils.random_sleep()
            return self.search(name, url=url)

        except Exception as ex:
            self.logger.error(ex)

    def _check_empty_google_results(self, soup):
        try:
            not_found_msg = soup.find('div', class_="med card-section")
        except:
            pass
        if not_found_msg is not None:
            return "done"
