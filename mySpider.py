# _*_ coding: utf-8 _*_


from spider_core import *


def runTest():

    # 读取配置文件
    max_repeat, crawl_interval, crawl_timeout, max_depth, url, fetcher_num, url_pattern, output_directory=conf.conf()

    # 定义fetcher parser saver urlFilter,支持自定义
    fetcher = Fetcher(max_repeat=max_repeat,crawl_interval=crawl_interval,crawl_timeout=crawl_timeout)
    parser = Parser(max_depth=max_depth,url_pattern=url_pattern)
    saver = Saver(output_directory=output_directory)
    url_filter=UrlFilter(black_patterns='')

    # 定义线程池
    spider=ThreadPool(fetcher=fetcher,parser=parser,saver=saver,url_filter=url_filter,fetcher_num=fetcher_num)
    spider.set_start_url(url=url,priority=0,deep=0)
    print("start")
    spider.execute()
    spider.wait_for_finish()
    print("end")
    return

if __name__ == '__main__':
    runTest()
    exit()





