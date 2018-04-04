# _*_ coding: utf-8 _*_

import sys
from spider_core import log
from spider_core import conf

class Saver(object):

    def __init__(self,output_directory):
        """
        :param output_directory:
        """
        self._output_directory=output_directory
        return

    def run(self, url: str, item: (list, tuple)) -> int:
        """
        保存parser的解析结果到指定方式中
        :param url: 所属url
        :param item: parser返回的解析结果
        :return:save_result: can be -1(save failed), 1(save success)
        """
        log.logger.debug("%s start: url=%s", self.__class__.__name__, url)
        try:
            save_result = self.item_save(url,  item)
        except Exception as excep:
            save_result = -1
            log.logger.error("%s error: %s,url=%s", self.__class__.__name__, excep,  url)

        log.logger.debug("%s end: save_result=%s, url=%s", self.__class__.__name__, save_result, url)
        return save_result

    def item_save(self, url: str,item) -> int:
        """
        具体的保存逻辑。支持重写自定义实现
        :param url: 所属url
        :param item: parser返回的解析对象
        :return:
        """
        self._save_pipe.write("\t".join([str(col) for col in item]) + "\n")
        self._save_pipe.flush()
        return 1

    def item_save(self, url: str,item):
        path = self._output_directory+"/"+url.replace('/', '_').replace(':', '_').replace('?', '_').replace('\\', '_')+".html"
        save_pipe = open(path,"w").write(item[1])
        save_pipe.flush()
        save_pipe.close()