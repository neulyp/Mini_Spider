# _*_ coding: utf-8 _*_

from spider_core import log
from spider_core import conf
from bs4 import BeautifulSoup # 解析html
import re # 正则
import datetime # 日期


class Parser(object):

    def __init__(self,max_depth=0,url_pattern=".*"):
        """
        :param max_depth: 爬虫最大深度
        """
        self._max_depth=max_depth
        self._url_pattern=url_pattern
        return

    def run(self, priority: int, url: str, deep: int, content: object) -> (int, list, list):
        """

        :param priority: 优先级，解释同fetcher
        :param url: 所属url
        :param deep: 当前遍历深度
        :param content: 需要解析的内容，由fetcher返回的content决定。
        :return: (int, list, list)：解析状态 -1/failed 1/success 解析返回的url列表 解析出来需要保存的内容
        """

        log.logger.debug("%s start: %s", self.__class__.__name__, conf.CONFIG_PARSE_MESSAGE % (priority, deep, url))

        try:
            parse_result, url_list, save_list = self.htm_parse(priority, url,  deep, content)
        except Exception as excep:
            parse_result, url_list, save_list = -1, [], []
            log.logger.error("%s error: %s, %s", self.__class__.__name__, excep, conf.CONFIG_PARSE_MESSAGE % (priority, deep, url))

        log.logger.debug("%s end: parse_result=%s, len(url_list)=%s, len(save_list)=%s, url=%s", self.__class__.__name__, parse_result, len(url_list), len(save_list), url)
        return parse_result, url_list, save_list

    def htm_parse(self, priority: int, url: str, deep: int, content: object) -> (int, list, list):
        """
        具体的解析逻辑，返回解析状态，解析出来的url列表，需要保存的context列表
        支持重写，实现自己的逻辑

        :param priority:
        :param url:
        :param deep:
        :param content:需要解析的内容，由fetcher返回的content决定。 fetcher中实现 返回的context=（status_code, url_now, html_text）
        :return:
        """
        status_code, url_now, html_text = content
        url_list = []
        # 判断当前深度是否小于最大深度
        if deep < self._max_depth:
            bs = BeautifulSoup(html_text, 'lxml')
            # 找出所有a标签href属性的值，将其加入到list中，优先级+1。 保存为url/priority 这样子的键值对
            # @TODO 提到的判断是否是绝对路径 还是相对路径
            #for link in bs.find_all(name='a', attrs={"href": re.compile(r'^http:|')}):
            for link in bs.find_all('a'):
                url_list.append((link.get('href'),priority+1))
        # @TODO 解析内容，将需要保存的内容放到save_list中
        save_list=[]
        # 此刻我们的需求是保存整个网页，因此，我们保存为url/html_text 这样子的键值对
        if html_text :
            save_list=[(url,html_text),]
        else:
            save_list=[]
        return 1,url_list,save_list







