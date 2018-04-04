# _*_ coding: utf-8 _*_

import enum
import threading
import queue

from spider_core import log


class TaskType(enum.Enum):
    """
    任务类型：主要包括请求，解析，保存三种
    """
    TASK_FETCH = "task_fetch"
    TASK_PARSE = "task_parse"
    TASK_SAVE = "task_save"


class BaseThread(threading.Thread):
    """
    线程基类
    """

    def __init__(self, name, worker, pool):
        """

        :param name: 线程名称
        :param worker: 实际工作者
        :param pool:
        """
        threading.Thread.__init__(self, name=name)
        self._worker = worker
        self._pool = pool
        return

    def run(self):
        while True:
            try:
                if not self.execute_job():
                    break
            except (queue.Empty, TypeError):
                # @TODO 有一点疑问，如果队列为空，说明此时没有任务，如果所有任务完成，那么就结束运行。
                if self._pool.get_thread_stop_flag() and self._pool.is_all_task_done():
                    break
            except Exception as excep:
                log.logger.error("%s[%s] error: %s", self.__class__.__name__, self.getName(), excep)
                break

        log.logger.debug("%s[%s] end...", self.__class__.__name__, self.getName())
        return

    def execute_job(self):
        """
        procedure of each thread, return True to continue, False to stop
        :return:
        """
        raise NotImplementedError


class FetchThread(BaseThread):
    """
    继承BaseThread，主要实现fetch的具体流程逻辑
    """

    def __init__(self, name, worker, pool):
        """
        初始化
        :param name:
        :param worker:
        :param pool:
        """
        BaseThread.__init__(self, name, worker, pool)
        self._proxies = None
        return

    def execute_job(self):

        # 获取fetch task
        priority, url, deep, repeat = self._pool.get_task(TaskType.TASK_FETCH)
        fetch_result, proxies_state, content = self._worker.run(priority, url, deep, repeat, proxies=self._proxies)

        # 根据处理结果添加任务
        if fetch_result > 0:
            self._pool.add_task(TaskType.TASK_PARSE, (priority, url, deep, content))
        elif fetch_result == 0:
            self._pool.add_task(TaskType.TASK_FETCH, (priority + 1, url, deep, repeat + 1))
        elif fetch_result < 0:
            print()
        # 结束任务
        self._pool.finish_task(TaskType.TASK_FETCH)
        return True


class ParseThread(BaseThread):
    """
    继承BaseThread，定义parse线程的行为
    """

    def execute_job(self):

        priority, url, deep, content = self._pool.get_task(TaskType.TASK_PARSE)
        parse_result, url_list, save_list = self._worker.run(priority, url, deep, content)
        # 如果解析成功parse_result=，那么添加save任务和fetch任务
        if parse_result == 1:
            for _url, _priority in url_list:
                # 深度+1 repeat设置为0
                self._pool.add_task(TaskType.TASK_FETCH, (_priority, _url, deep + 1, 0))
            for item in save_list:
                # 数据结构为（url,item）
                self._pool.add_task(TaskType.TASK_SAVE, (url, item))
        else:
            print()
        self._pool.finish_task(TaskType.TASK_PARSE)
        return True


class SaveThread(BaseThread):
    """
    继承BaseThread，定义save线程的行为
    """

    def execute_job(self):

        # 获取context
        url, item = self._pool.get_task(TaskType.TASK_SAVE)

        # 执行task
        save_result = self._worker.run(url, item)

        self._pool.finish_task(TaskType.TASK_SAVE)
        return True
