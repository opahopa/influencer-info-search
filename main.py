import time
import csv
import logging
from random import randint

from custom_threading import MyExecutor
from scraping.scrape_job import InfoScraper
from logging.config import fileConfig

from scraping.data_singleton import DataSingleton

dataCache = DataSingleton()

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

thread_count = 1


def _test_check():
    sleep_time = randint(0, 9)
    time.sleep(sleep_time)
    print(str(time.time()) + " just slept {} sec".format(sleep_time))
    return


def _test_main():
    executor = MyExecutor(thread_count, _test_check)
    executor.start()

    time.sleep(20)
    executor.stop()
    return


def save_result_to_csv(results_list):
    logger.info("writing results: %s" % len(results_list))
    if len(results_list) > 0:
        try:
            with open('result.csv', 'w', encoding='utf-8') as csvfile:

                keys = ['name', 'facebook', 'twitter', 'instagram', 'linkedin', 'other', 'domains', 'emails']
                writer = csv.DictWriter(csvfile, quoting=csv.QUOTE_ALL, delimiter=',', lineterminator='\n',
                                        fieldnames=keys)

                writer.writeheader()
                for seo_result in results_list:
                    csv_dict = seo_result.to_csv_dict()  # don`t call csv dict multiple times!
                    print(csv_dict)
                    writer.writerow(csv_dict)

            return True

        except Exception as ex:
            logger.error(ex)
            return False


def scrape_main():
    _info_scraper = InfoScraper()

    try:
        executor = MyExecutor(thread_count, _info_scraper.scrape_main)
        futures = executor.start()

        executor.shutdown_executor(wait=True)

        save_result_to_csv(dataCache.results_list)
        return True
    except:
        pass


def _validate_console_input(num_input):
    try:
        val = int(num_input)
        if val % 1 == 0 & val < 15:
            return True
        else:
            return False
    except ValueError:
        print("That's not a number!")
        return False


if __name__ == "__main__":
    thread_count = int(input("Threads number(max 500):"))
    if _validate_console_input(thread_count) is True:
        print("Thread count: ", thread_count)
        input("Press Enter to start...")

        scrape_main()
    else:
        print("Wrong format")
