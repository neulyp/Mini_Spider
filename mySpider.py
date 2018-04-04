# _*_ coding: utf-8 _*_

import sys
import getopt
from spider_core import *
from spider_core import conf

# def runTest():
#
#     # 读取配置文件
#     max_repeat, crawl_interval, crawl_timeout, max_depth, url, fetcher_num, url_pattern, output_directory=conf.conf()
#
#     # 定义fetcher parser saver urlFilter,支持自定义
#     fetcher = Fetcher(max_repeat=max_repeat,crawl_interval=crawl_interval,crawl_timeout=crawl_timeout)
#     parser = Parser(max_depth=max_depth,url_pattern=url_pattern)
#     saver = Saver(output_directory=output_directory)
#     url_filter=UrlFilter(black_patterns='')
#
#     # 定义线程池
#     spider=ThreadPool(fetcher=fetcher,parser=parser,saver=saver,url_filter=url_filter,fetcher_num=fetcher_num)
#     spider.set_start_url(url=url,priority=0,deep=0)
#     print("start")
#     spider.execute()
#     spider.wait_for_finish()
#     print("end")
#     return

# if __name__ == '__main__':
#     runTest()
#     exit()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],"vhc")
    except getopt.GetoptError as err:
        print(err)
        return
    for a,o in opts:
        if a == "-v":
            print("version: 1.0  author: lyp")
            sys.exit()
        elif a =="-h":
            print("Usage:%s [-v|-h|-c] ....",sys.argv[0]);
            sys.exit()
        elif a =="-c":
            _max_repeat, _crawl_interval, _crawl_timeout, _max_depth, _fetcher_num, _url_pattern, _output_directory, url_seeds =conf()
            print("max_repeat:",_max_repeat)
            print("crawl_interval:", _crawl_interval)
            print("crawl_timeout:", _crawl_timeout)
            print("max_depth:", _max_depth)
            print("fetcher_num:", _fetcher_num)
            print("output_directory:", _output_directory)
            print("url_seeds:", url_seeds)
            sys.exit()
        else:
            print("no argvs")
            sys.exit()
    pool = core_threads_pool.create_pool()
    pool.execute()
    pool.wait_for_finish()
    return

if __name__ == '__main__':
    main()





