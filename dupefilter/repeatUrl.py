import threading
import datetime


class RepeatUrl:
    def __init__(self):
        self.visited_url = set()
        self.visLock = threading.Lock()

    @classmethod
    def from_settings(cls, settings):
        """
        初始化时，调用
        :param settings: 
        :return: 
        """
        return cls()

    def request_seen(self, request):
        """
        检测当前请求是否已经被访问过
        :param request: 
        :return: True表示已经访问过；False表示未访问过
        """
        self.visLock.acquire()
        url = request.url.strip()
        if url in self.visited_url:
            self.visLock.release()
            return True
        self.visited_url.add(url)
        self.visLock.release()
        return False

    def open(self):
        """
        开始爬去请求时，调用
        :return: 
        """
        pass

    def close(self, reason):
        """
        结束爬虫爬取时，调用
        :param reason: 
        :return: 
        """
        print("\r\n扫描结束，共扫描页面：%d个。\r\n" % len(self.visited_url))
        print("写入扫描历史记录...\r\n")
        with open('scan-history_%s.txt' % datetime.datetime.now().strftime("%Y%m%d%H%M%S"), 'w+') as fs:
            fs.write('\r'.join(self.visited_url))
        pass

    def log(self, request, spider):
        """
        记录日志
        :param request: 
        :param spider: 
        :return: 
        """
        pass
