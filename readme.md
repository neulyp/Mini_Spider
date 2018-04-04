
架构设计:
               urls
                |
                \/
       ---_queue_fetch<---
       |                 |
       \/                |
    Fetcher              |------>_queue_save            
       |                 |            | 
       \/                |            \/
   _queue_parse--------Parser       Saver------>File
   
1. 获取url列表，放入队列中。
2. fetcher线程从queue_fetch获取url 进行请求,请求结果放入队列queue_parse
3. parser线程从queue_parse获取context 进行解析，解析结果包含url_list和conetxt_list，分别放入队列中
4. saver线程从queue_save获取context_list 进行存储

使用方法：
继承Fetcher，Parser，Saver类，实现内部方法。demo见mySpider。
