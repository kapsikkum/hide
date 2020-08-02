import requests
from termcolor import colored

from hide import utils, values


def check_proxy(proxy, timeout, kind):
    s = requests.Session()
    if kind == "http":
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
    elif kind == "socks4":
        proxies = {
            "http": f"socks4://{proxy}",
            "https": f"socks4://{proxy}"
        }
    elif kind == "socks5":
        proxies = {
            "http": f"socks5://{proxy}",
            "https": f"socks5://{proxy}"
        }
    try:
        src = s.get("https://www.google.com/", proxies=proxies, timeout=int(timeout))
    except Exception as e:
        values.bad_proxies.append(proxy)
        values.print_queue.append(colored(f"[{proxy}]: Bad", "red"))
    else:
        if src.status_code == 200:
            values.good_proxies.append(proxy)
            values.to_write.append(proxy)
            values.print_queue.append(colored(f"[{proxy}]: Good", "green"))
        else:
            values.bad_proxies.append(proxy)
            values.print_queue.append(colored(f"[{proxy}]: Bad", "red"))
