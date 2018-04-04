# _*_ coding: utf-8 _*_

import queue  # 队列
import copy  # 拷贝对象 用于创建线程池中线程
from .core_threads import TaskType, FetchThread, ParseThread, SaveThread


class ThreadPool(object):
    """
    线程池
    """

    def __init__(self, fetcher, parser, saver, url_filter, fetcher_num=10):

        # 线程类型
        self._inst_fetcher = fetcher  # fetcher instance, subclass of Fetcher
        self._inst_parser = parser  # parser instance, subclass of Parser
        self._inst_saver = saver  # saver instance, subclass of Saver

        # 队列 主要包含fetch parse save
        self._queue_fetch = queue.PriorityQueue()  # (priority, url, deep, repeat)
        self._queue_parse = queue.PriorityQueue()  # (priority, url, deep, content)
        self._queue_save = queue.Queue()  # (url, item), item can be anything

        # 线程列表 包含请求fetch 和 解析存储 parsar 两类
        self._thread_fetcher_list = []  # fetcher threads list
        self._thread_parsar_list = []  # parser and saver threads list

        # url 过滤器
        self._url_filter = url_filter  #

        # 线程池是否结束flag
        self._thread_stop_flag = False  # default: False, stop flag of threads

        # 线程池中fetch线程个数
        self._fetcher_num = fetcher_num

        return

    def set_start_url(self, url, priority=0, deep=0, repeat=0):
        """
        设置起始url，添加一个fetch任务
        :param url:
        :param priority:
        :param deep:
        :param repeat:
        :return:
        """
        self.add_task(task_type=TaskType.TASK_FETCH, task_content=(priority, url, deep, repeat))
        return

    def execute(self):
        """
        执行线程池
        :return:
        """

        # 初始化fetch thread列表
        self._thread_fetcher_list = []
        for i in range(self._fetcher_num):
            self._thread_fetcher_list.append(
                FetchThread(name="fetcher-%d" % (i + 1), worker=copy.deepcopy(self._inst_fetcher), pool=self))

        # 初始化parser thread列表
        self._thread_parsar_list.append(ParseThread(name="parser", worker=self._inst_parser, pool=self))
        self._thread_parsar_list.append(SaveThread(name="saver", worker=self._inst_saver, pool=self))

        # 设置daemon
        for thread in self._thread_fetcher_list:
            thread.setDaemon(True)
            thread.start()

        for thread in self._thread_parsar_list:
            thread.setDaemon(True)
            thread.start()
        return

    def wait_for_finish(self):

        self._thread_stop_flag = True

        for thread in self._thread_fetcher_list:
            if thread.is_alive():
                thread.join()

        for thread in self._thread_parsar_list:
            if thread.is_alive():
                thread.join()

        return

    def add_task(self, task_type, task_content):
        """

        :param task_type: 任务类型
        :param task_content: 任务context
        :return:
        """

        # 当一个任务类型是fetch 并且url从未解析过 或者url已经请求过但是在重试次数范围内 添加一个fetch task
        if task_type == TaskType.TASK_FETCH and (
                task_content[-1] > 0 or self._url_filter.check_and_add(task_content[1])):
            self._queue_fetch.put_nowait(task_content)
        elif task_type == TaskType.TASK_PARSE:
            self._queue_parse.put_nowait(task_content)
        elif task_type == TaskType.TASK_SAVE:
            self._queue_save.put_nowait(task_content)
        print("fetch queue: %s",self._queue_fetch.qsize())
        print("parse queue: %s",self._queue_parse.qsize())
        print("save queue: %s",self._queue_save.qsize())
        print()
        return

    def get_task(self, task_type):
        task_c = None
        if task_type == TaskType.TASK_FETCH:
            task_c = self._queue_fetch.get(block=True, timeout=5)
            return task_c
        elif task_type == TaskType.TASK_PARSE:
            task_c = self._queue_parse.get(block=True, timeout=5)
            return task_c
        elif task_type == TaskType.TASK_SAVE:
            task_c = self._queue_save.get(block=True, timeout=5)
            return task_c
        print("fetch queue: %s",self._queue_fetch.qsize())
        print("parse queue: %s",self._queue_parse.qsize())
        print("save queue: %s",self._queue_save.qsize())
        print()
        return task_c

    def finish_task(self, task_type):
        if task_type == TaskType.TASK_FETCH:
           self._queue_fetch.task_done()
        elif task_type == TaskType.TASK_PARSE:
            self._queue_parse.task_done()
        elif task_type == TaskType.TASK_SAVE:
            self._queue_save.task_done()
        return

    def get_thread_stop_flag(self):
        return self._thread_stop_flag

    def is_all_task_done(self):
        return self._queue_save.empty() and self._queue_parse.empty() and self._queue_fetch.empty()
