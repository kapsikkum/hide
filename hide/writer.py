from hide import values


def write_scrape_to_file(listname):
    string = str()
    for proxy in set(values.found_proxies):
        string += f"{proxy}\n"
    with open(f"proxies/scraped/{listname}", "a") as f:
        f.write(string)


def write_proxy_to_file(proxy, listname):
    with open(f"proxies/checked/{listname}", "a") as f:
        f.write(f"{proxy}\n")


def checker_write_thread(listname):
    while values.checking_proxies:
        for proxy in values.to_write:
            write_proxy_to_file(proxy, listname)
            values.to_write.remove(proxy)
