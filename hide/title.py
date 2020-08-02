import ctypes
import sys
import time

import hide
from hide import values


def change_title(text):
    if sys.platform.startswith('win32'):
        ctypes.windll.kernel32.SetConsoleTitleW(text)
    else:
        sys.stdout.write(f"\x1b]2;{text}\x07")


def scraper_title():
    while values.scraping_proxies:
        change_title(f"hide!v{hide.__version__} | Scraping Proxies: {len(values.found_proxies)} found total.")
        time.sleep(0.5)


def checker_title():
    while len(values.to_check) < 1:
        time.sleep(1)
    total = len(values.to_check)
    while values.checking_proxies:
        total_finished = len(values.good_proxies) + len(values.bad_proxies)
        remaining = total - total_finished
        change_title(
            f"hide!v{hide.__version__} | Checking Proxies | {len(values.good_proxies)} Good | {len(values.bad_proxies)} Bad | Remaining: {remaining} | Total: {len(values.good_proxies) + len(values.bad_proxies)}/{total}")
        time.sleep(0.5)
