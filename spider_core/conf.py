# _*_ coding: utf-8 _*_

from spider_core.log import logger
import configparser
import os

# define the structure of message, used in Fetcher and Parser
CONFIG_FETCH_MESSAGE = "priority=%s, deep=%s, repeat=%s, url=%s"
CONFIG_PARSE_MESSAGE = "priority=%s, deep=%s, url=%s"

# define url_pattern
CONFIG_URL_PATTERN = r"\.(cab|iso|zip|rar|tar|gz|bz2|7z|tgz|apk|exe|app|pkg|bmg|rpm|deb|dmg|jar|jad|bin|msi|" \
                     "pdf|doc|docx|xls|xlsx|ppt|pptx|txt|md|odf|odt|rtf|py|java|c|cc|js|css|log|" \
                     "jpg|jpeg|png|gif|bmp|xpm|xbm|ico|drm|dxf|eps|psd|pcd|pcx|tif|tiff|" \
                     "mp3|mp4|swf|mkv|avi|flv|mov|wmv|wma|3gp|mpg|mpeg|mp4a|wav|ogg|rmvb)$"


def conf():
    cp = configparser.ConfigParser()
    path = r'/Users/loren/PycharmProjects/Mini_Spider/spider_core/spider.conf'
    try:
        cp.read(path)
    except Exception as err:
        logger.error("get conf file error: %s" % err)
        return
    try:
        max_repeat = cp.getint("spider", "max_repeat")
        crawl_interval = cp.getint("spider", "crawl_interval")
        crawl_timeout = cp.getint("spider", "crawl_timeout")
        max_depth = cp.getint("spider", "max_depth")
        url = cp.get("spider", "url")
        fetcher_num = cp.getint("spider", "fetcher_num")
        url_pattern = cp.get("spider", "url_pattern")
        output_directory = cp.get("spider", "output_directory")
    except Exception as err:
        logger.error("conf file format error: %s" % err)
        return

    return max_repeat, crawl_interval, crawl_timeout, max_depth, url, fetcher_num, url_pattern, output_directory
