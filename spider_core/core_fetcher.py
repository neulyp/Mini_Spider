# _*_ coding: utf-8 _*_

from spider_core import log
from spider_core import conf
import time
import requests  # http请求


class Fetcher(object):

    def __init__(self, max_repeat=3, crawl_interval=1, crawl_timeout=2):
        """
        该类主要请求url，并返回请求内容。提供
        :param max_repeat: 最大重试次数
        :param crawl_interval: 爬去间隔
        :param crawl_timeout: 超时设置
        """

        self._max_repeat = max_repeat
        self._crawl_interval = crawl_interval
        self._crawl_timeout = crawl_timeout

    def run(self, priority: int, url: str, deep: int, repeat: int, proxies=None) -> (int, bool, object):
        """

        :param priority: 每次请求都有优先级，数字越小，优先级越高；跟节点优先级为0，请求失败重试一次，priority+1；deep+1，priority+1。
        :param url:请求的url
        :param deep:遍历深度
        :param repeat:第几次重复；没有重复为0，每重复一次+1
        :param proxies:代理
        :return:(int, bool, object)：请求结果-1(fetch failed), 0(need repeat), 1(fetch success)  代理状态 结果内容
        """
        log.logger.info("%s start: %s", self.__class__.__name__,
                        conf.CONFIG_FETCH_MESSAGE % (priority, deep, repeat, url))
        time.sleep(self._crawl_interval)

        try:
            fetch_result, proxies_state, content = self.url_fetch(priority, url, deep, repeat, proxies=proxies)
        except Exception as excep:
            if repeat >= self._max_repeat:
                # 请求失败，如果超过最大重试次数，fetch_result=-1
                fetch_result, proxies_state, content = -1, False, None
                log.logger.error("%s error: %s, %s", self.__class__.__name__, excep,
                                 conf.CONFIG_FETCH_MESSAGE % (priority, deep, repeat, url))
            else:
                # 请求失败，如果未超过最大重试次数，需要重试, fetch_result=0
                fetch_result, proxies_state, content = 0, False, None
                log.logger.debug("%s repeat: %s, %s", self.__class__.__name__, excep,
                                 conf.CONFIG_FETCH_MESSAGE % (priority, deep, repeat, url))

        log.logger.info("%s end: fetch_result=%s, proxies_state=%s, url=%s", self.__class__.__name__, fetch_result,
                        proxies_state, url)

        return fetch_result, proxies_state, content

    def url_fetch(self, priority: int, url: str, deep: int, repeat: int, proxies=None) -> (int, bool, object):
        """
        fetch 核心方法，可以重写该方法实现自定义逻辑。
        :param priority:
        :param url:
        :param deep:
        :param repeat:
        :param proxies:
        :return:
        """
        response = requests.get(url=url, params=None, headers={}, data=None, proxies=proxies,
                                timeout=self._crawl_timeout)
        content = (response.status_code, response.url, response.text)
        return 1, True, content

