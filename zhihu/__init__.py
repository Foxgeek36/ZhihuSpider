import math

from util import timer

SLEEP = 5


class Controller:
    def __init__(self, crawl_times=-1, limit=20):
        self.totals = -1  # 总数
        self.offset = 0  # 起始
        self.limit = limit  # 每次下载的数量
        self.inf_counter = 0  # 非优质回答计数器
        self.stop = False  # 停止控制器
        self.crawl_times = crawl_times  # 最大爬取数量
        self.crawl_counter = 0  # 爬取数量计数器，（收录和未收录的总数）

    def increase(self, num=None):
        if num is None:
            self.offset += self.limit
        else:
            self.offset += num
        self.crawl_counter = self.offset
        if self.totals != -1 and self.crawl_counter >= self.totals:
            self.to_stop()
            return
        if self.crawl_times == -1:
            return
        if self.crawl_counter >= self.crawl_times:
            self.to_stop()

    def next_offset(self):
        return self.offset

    def is_end(self):
        return self.stop

    def inferior_counter(self):
        self.inf_counter += 1
        if self.inf_counter == 200:
            self.to_stop()

    def init_counter(self):
        self.inf_counter = 0

    def to_stop(self):
        self.stop = True

    def __str__(self):
        return 'totals: {}, offset:{}, limit: {}'.format(self.totals, self.offset, self.limit)

    def to_collect(self, answer_content):
        n = timer.timestamp()
        v = answer_content['voteup_count']
        c = answer_content['created_time']
        u = answer_content['updated_time']
        collect = evaluate(v, c, u, n) > 0.5
        if not collect:
            self.inferior_counter()
            if not self.is_end() and v > 200:
                self.init_counter()
        else:
            self.init_counter()
        return collect

    def running_status(self, is_end: bool = False):
        if is_end:
            self.to_stop()


def evaluate(v, c, u, n):
    g = 1 - (1 / math.log10(v + 10))
    x = 3600 * (v / (n - c))
    e = ((1 / (pow(math.e, - x / 2) + 1)) - 0.5) * 2
    p = (u - c) / (n - c) if n - c > 10000 else 0
    return 0.7 * g + 0.2 * e + 0.1 * p


"""
说明：
    zhihu 是功能模块，所有要实现的功能（爬取专栏、文章等）都在这个模块下实现。
    实现的功能：article、collection、question、topic、user
    其中article实现了单篇文章或专栏的爬取，question实现了单个或所有回答的爬取，user实现了针对用户的所有文章和所有回答
的爬取。这些模块之间并不是完全独立的，比如collection既有问答又有文章，在实现时使用了article模块的article和question
模块的answer。
    本文件实现了Controller和evaluate，前者用于爬取控制，控制程序的停止、爬取目标的下一页等，后者用于计算回答的评分，根
据评分决定一个问题的某个回答是否收录。
"""
