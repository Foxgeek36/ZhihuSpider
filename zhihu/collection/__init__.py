# 首先通过api获得收藏夹的信息 -- 收藏项目总数，根据总数计算页数（每页10条）
# 利用页数构造url访问，获得 html 文本

# 方案1：
# 解析锁定 contents = <div id="zh-list-collection-wrap" style="margin-bottom: 10px;">
# 对 contents 遍历，contents 的子标签是包含目标内容的标签
# 获得作者等有关信息，封装成字典，文章主体通过处理 textarea 标签获得
# 优点：相对于方案2，减少了网络请求次数，从而加快了任务速度，资源有效利用率高
# 缺点：信息提取难度大，信息不完整，其中文章不包含创作时间

# 方案2：
# 使用正则表达式在网页中搜索文章、回答的访问链接，进一步提取相应的id，利用id通过api获得内容，从而实现功能
# 优点：实现简单，可以利用已实现的 article 和 answer 来完成任务
# 缺点：网络访问次数增多，拖慢程序整体速度，有一定风险（封IP）

# 方案3：
# 结合方案1和方案2，提取html中的回答部分，完成回答的抓取，提取文章id，通过article完成任务
# 优点：减少网络访问次数，速度有所加快

# 方案4：
# 按方案1操作，缺失的信息置为空

import os
import re

from util import net
from zhihu.article import article
from zhihu.question import answer


def collection_msg(collection_id: str, warehouse: str):
    response = net.collection_msg_spider(collection_id)
    if response is not None:
        response_json = response.json()
        item_count = response_json['item_count']
        name = response_json['title']
        warehouse = os.path.join(warehouse, name)
        if not os.path.exists(warehouse):
            os.makedirs(warehouse)
        return item_count, warehouse
    else:
        raise ValueError('Response is None')


def collection(collection_id: str, warehouse: str):
    """获得收藏夹的信息，计算、构造url，并访问url，获得html，之后开始解析。"""
    item_count, warehouse = collection_msg(collection_id, warehouse)
    pages = item_count // 10 + 2
    for page in range(1, pages):
        if page == 10:
            break
        response = net.collection_spider(collection_id, page)
        if response is not None:
            content = response.text
            articles_id = re.findall(r'<link itemprop="url" href="https://zhuanlan.zhihu.com/p/(\d+)">', content)
            for article_id in articles_id:
                a = article(article_id, warehouse)
                print(a)
            answers_id = re.findall(r'<link itemprop="url" href="/question/\d+/answer/(\d+)">', content)
            for answer_id in answers_id:
                a = answer(answer_id, warehouse)
                print(a)
        else:
            raise ValueError('Response is None')


if __name__ == '__main__':
    c_id = '273369749'
    native_warehouse = r"C:\Users\Milloy\Desktop"
    collection(c_id, native_warehouse)


"""
说明：
    收藏夹没有获取内容主体的api，这里采用上方给出的方案2实现，逻辑比较简单。
"""

