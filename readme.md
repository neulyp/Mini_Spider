需求：

- 【必须】需要支持命令行参数处理。具体包含: -h(帮助)、-v(版本)、-c(配置文件)
- 【必须】需要按照广度优先的顺序抓取网页。
- 【必须】单个网页抓取或解析失败，不能导致整个程序退出。需要在日志中记录下错误原因并继续。
- 【必须】从HTML提取链接时需要处理相对路径和绝对路径。
- 【必须】网页存储时每个网页单独存为一个文件，以URL为文件名。注意对URL中的特殊字符，需要做转义。
- 【必须】要求支持多线程并行抓取。
- 【必须】代码的可读性和可维护性好。注意模块、类、函数的设计和划分
- 
- 【可选】当程序完成所有抓取任务后，优雅退出。
- 【可选】需要能够处理不同字符编码的网页(例如utf-8或gbk)。
- 【可选】完成相应的单元测试和使用demo。你的demo必须可运行，单元测试有效而且通过
- 【可选】可控制抓取间隔和总量，避免对方网站封禁IP。

运行环境：
anaconda3 / python3

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
实际的url过滤见UrlFilter 中的设置，比如内部默认实现为只保留http开头的url

运行：
python ./mySpider.py

改进（抽时间加一下，这两块应该比较容易）：
- 【必须】从HTML提取链接时需要处理相对路径和绝对路径。
- 【可选】需要能够处理不同字符编码的网页(例如utf-8或gbk)。

