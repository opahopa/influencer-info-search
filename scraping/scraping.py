import logging
import re
import sys
import threading

from urllib.parse import urlsplit
from scraping.data_singleton import DataSingleton
from scraping.search.google_search import GoogleSearch
from scraping.search.other_search import OtherSearch
from .models import InfoResult


class ScrapeFactory:
    lock = threading.Lock()

    dataCache = DataSingleton()

    def __init__(self, proxy=None):
        self.logger = logging.getLogger(__name__)
        self._proxy = proxy

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._proxy = None

    def run_info_search(self, name):
        try:
            google_search = GoogleSearch(self._proxy)
            google_urls = google_search.search(name)
            match_urls = self.parse_google_urls(google_urls, name)

            # for match in match_urls:
            #     print(match)

            other_search = OtherSearch(self._proxy)
            domains = other_search.search_domains(name)
            emails = other_search.search_emails(domains)

            return InfoResult(name, match_urls=match_urls, domains=domains, emails=emails)
            # self.save_result_to_csv(result)


        except Exception:
            print("appending name back")
            self.dataCache.names_list.append(name)
            self.logger.debug("Unexpected error:", sys.exc_info()[0])
            return None

    def parse_google_urls(self, google_urls, name):
        match_urls = []
        for url in google_urls:
            url_temp = re.sub(r'[-_+]', " ", url['url'], flags=re.IGNORECASE)
            title_temp = url['title']
            try:
                if name.lower() in url_temp.lower() and url_temp.lower().startswith('http') or "".join(
                        name.lower().split()) in url_temp.lower() and url_temp.lower().startswith('http'):
                    match_urls.append(url['url'][:url['url'].find('&')])

                if name.lower() in title_temp.lower() and bool([el for el in match_urls if "{0.scheme}://{0.netloc}/".format(urlsplit(url['url'])) not in el]):
                    match_urls.append(url['url'][:url['url'].find('&')])
            except:
                pass

        return match_urls
