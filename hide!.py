import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from tkinter import *
from tkinter.filedialog import *

from colorama import init
from termcolor import colored

import hide
from hide import checker, scraper, title, utils, values, writer

Tk().withdraw()
menu = colored("""
  
                 ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄  ▄ 
                ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░▌
                ▐░▌       ▐░▌ ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌
                ▐░▌       ▐░▌     ▐░▌     ▐░▌       ▐░▌▐░▌          ▐░▌
                ▐░█▄▄▄▄▄▄▄█░▌     ▐░▌     ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌
                ▐░░░░░░░░░░░▌     ▐░▌     ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌
                ▐░█▀▀▀▀▀▀▀█░▌     ▐░▌     ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌
                ▐░▌       ▐░▌     ▐░▌     ▐░▌       ▐░▌▐░▌           ▀ 
                ▐░▌       ▐░▌ ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄  ▄ 
                ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░▌
                 ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀▀▀▀▀  ▀ 
""", "blue")                                 

options = colored("""

        1.  Scrape Proxies
        2.  Check Proxies

""", "blue")

if __name__ == "__main__":
    threading.Thread(target=utils.auto_print_thread, daemon=True).start()
    init()
    while True:
        utils.clear()
        utils.reset_values()
        title.change_title(f"hide!v{hide.__version__}")
        print(menu)
        print(options)
        i = input(colored("> ", "blue"))
        if i == "1":
            utils.clear()
            print(menu)
            i = input("\nUse Custom Proxy Site List? <y/n>: ")
            if i == "0":
                pass
            else:
                if i.lower() == "y":
                    filepath = askopenfilename(initialdir=os.getcwd(), title="Select Text File",
                                               filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
                    if os.path.isfile(filepath):
                        scrape_list = utils.parse_list(path=filepath, type="Local")
                    else:
                        scrape_list = utils.parse_list()
                else:
                    scrape_list = utils.parse_list()
                values.scraping_proxies = True
                threading.Thread(target=title.scraper_title, daemon=True).start()
                with ThreadPoolExecutor(max_workers=10) as executor:
                    for link in scrape_list:
                        executor.submit(scraper.scrape_link, link)
                values.scraping_proxies = False
                values.print_queue.append(colored(f"Found {len(values.found_proxies)} proxies total. \nWriting to file, Please wait...", "blue"))
                writer.write_scrape_to_file(
                    f'{datetime.now().strftime("%m-%d-%Y %H-%M-%S")}.txt')
                input(colored("Press enter to continue", "blue"))
        elif i == "2":
            utils.clear()
            filepath = askopenfilename(initialdir="proxies/scraped/", title="Select Proxy List",
                                       filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
            if os.path.isfile(filepath):
                thread = input(colored("Threads (Default: 100): ", "blue"))
                if not thread.isdigit():
                    thread = 100
                timeout = input(colored("Timeout (Default: 10): ", "blue"))
                if not timeout.isdigit():
                    timeout = 10
                kind = input(colored("Type of proxy: (0:http/s (Default), 1: socks4, 2: socks5): ", "blue"))
                if kind == "0":
                    kind = "http"
                elif kind == "1":
                    kind = "socks4"
                elif kind == "2":
                    kind = "socks5"
                else:
                    kind = "http"
                utils.clear()
                print(colored("Checker Starting...", "green"))
                values.checking_proxies = True
                threading.Thread(target=title.checker_title, daemon=True).start()
                filename, extension = utils.parse_filename(filepath)
                listname = f"{filename}-working{extension}"
                threading.Thread(target=writer.checker_write_thread, args=[listname], daemon=True).start()
                values.to_check = set(open(filepath).read().splitlines())
                with ThreadPoolExecutor(max_workers=int(thread)) as executor:
                    for proxy in set(values.to_check):
                        executor.submit(checker.check_proxy, proxy, int(timeout), kind)
                        values.to_check.remove(proxy)
                values.checking_proxies = False
                values.print_queue.append(colored(f"Good Proxies: {len(values.good_proxies)}, Bad Proxies:{len(values.bad_proxies)}", "blue"))
                while len(values.print_queue) > 0:
                    time.sleep(1)
                input(colored("Press enter to continue", "blue"))
