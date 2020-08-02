import os
import sys
import time

from requests import Session

from hide import values

req = Session()

def construct_proxy(proxy, port):
    return f"{proxy}:{port}"


def parse_filename(path):
    filename, extension = os.path.splitext(path)
    return filename.split("/")[-1], extension


def reset_values():
    values.bad_proxies = list()
    values.good_proxies = list()
    values.found_proxies = list()
    values.to_write = list()
    values.to_check = list()


if sys.platform.startswith("win32"):
    def clear(): return os.system("cls")
else:
    def clear(): return os.system("clear")


def parse_list(path="https://gist.githubusercontent.com/DeadBread76/608c733168cb808783d2024def3ea736/raw/db2d029485647a1033b07551453de47d8f9ed75e/Proxy%2520Sources%2520(Stolen%2520from%2520Proxyscrape%2520Scraper%2520lol).txt", type="Internet"):
    if type == "Local":
        return open(path).read().splitlines()
    elif type == "Internet":
        return req.get(path).text.splitlines()


def auto_print_thread():
    while True:
        for p in values.print_queue:
            print(p)
            values.print_queue.remove(p)
