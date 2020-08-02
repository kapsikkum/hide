import os

# make folders
if not os.path.isdir("proxies/"):
    os.mkdir("proxies/")
if not os.path.isdir("proxies/scraped/"):
    os.mkdir("proxies/scraped/")
if not os.path.isdir("proxies/checked/"):
    os.mkdir("proxies/checked/")

# version shit
__version_info__ = (1, 1, 1)
__version__ = '.'.join(map(str, __version_info__))

