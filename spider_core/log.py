# _*_ coding: utf-8 _*_

import logging

def get_logger(logfile):
    """
    :param logfile:日志文件
    :return:
    """
    logger = logging.getLogger(__name__)
    log_handler = logging.FileHandler(logfile)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    ll = (logging.CRITICAL,
          logging.ERROR,
          logging.WARNING,
          logging.INFO,
          logging.DEBUG)
    logger.setLevel(ll[4])
    log_handler.setLevel(ll[4])
    logger.addHandler(log_handler)
    return logger

logfile = 'sys_run.log'

logger = get_logger(logfile=logfile)
