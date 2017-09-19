import traceback
import logging
import requests
import re

from scraping.utils import Utils
from bs4 import BeautifulSoup


class OtherSearch(object):
    request_timeout = 10

    def __init__(self, proxy=None):
        self.logger = logging.getLogger(__name__)

        try:
            self._s = requests.Session()

            if proxy is not None:
                self._s.proxies = proxy.dict_for_requests()

            self._user_agent_string = Utils.get_random_browser_agent()

        except Exception:
            print(traceback.format_exc())

    def __exit__(self, exc_type, exc_value, traceback):
        self._pages_counter = 0

    def search_domains(self, name):
        domains = []
        try:
            r = self._s.get("http://viewdns.info/reversewhois/?q=" + name, verify=False, timeout=self.request_timeout)
            soup = BeautifulSoup(r.text, 'lxml')

            results_table = soup.find('table', {"border": "1"})
            results_list = results_table.find_all('tr')

            # print('Count: %s' % len(results_list))
            for result in results_list[1:]:
                try:
                    tds = result.find_all('td')
                    domains.append({'name': tds[0].text, 'created': tds[1].text})
                except:
                    pass

            return domains

        except Exception as ex:
            self.logger.error(ex)
            return domains

    def search_emails(self, domains_list):
        if len(domains_list) == 0:
            return []

        for domain in domains_list:
            if "http" not in domain['name']:
                url = 'http://'+domain['name']
            else:
                url = domain['name']

            print("Loading: %s" % url)

            emails = []
            try:
                r = self._s.get(url, verify=False, timeout=self.request_timeout)
                emails = re.findall(r'[\w.-]+@[\w.-]+', r.text)

                if len(emails) > 0:
                    for email in emails:
                        print("Email Found: %s" % email)

            except requests.exceptions.ConnectionError:
                pass
            except Exception as ex:
                self.logger.error(ex)
                pass

            return emails
