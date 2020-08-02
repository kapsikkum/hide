import re

import requests
from termcolor import colored

from hide import utils, values

proxy_regex = "[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\:[0-9]{1,4}"


def scrape_link(link):
    s = requests.Session()
    values.print_queue.append(colored(f"Scraping: {link}", "yellow"))
    try:
        page = s.get(link, timeout=10)
    except Exception:
        values.print_queue.append(colored(f"Unable to scrape {link}", "red"))
    else:
        proxies = re.findall(proxy_regex, page.text)
        values.found_proxies.extend(proxies)
        values.print_queue.append(colored(f"Found {len(proxies)} proxies on {link}", "green"))
