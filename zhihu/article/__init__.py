import os
from util import net
from util import const
from util import document
import re
import util.timer as timer
from bs4 import BeautifulSoup
import zhihu

__all__ = ['article', 'articles']

GET_ARTICLES_ID = '正在获取文章 ID ...'


def article(article_id, warehouse):
    response = net.article_spider(article_id)
    if response is not None:
        response_json = response.json()
        content = BeautifulSoup(response_json['content'], 'lxml').body
        msg = article_msg(response_json)
        an = document.Article(content, msg)
        an.make_markdown(warehouse)
        return an.article_msg()
    else:
        raise ValueError('Response is None')


def articles(column_id, warehouse):
    articles_list = articles_id(column_id)
    request_times = dict([(i, 0) for i in articles_list])
    warehouse = column_warehouse(column_id, warehouse)
    while len(articles_list) != 0:
        article_id = articles_list.pop(0)
        try:
            ar = article(article_id, warehouse)
            print(ar)
        except ValueError:
            if request_times.get(article_id) < 5:
                articles_list.append(article_id)
                request_times[articles_id] += 1
        timer.random_sleep(end=zhihu.SLEEP)
    for article_id, times in request_times.items():
        if times >= 5:
            print(net.article_spider_url(article_id))


def article_msg(content):
    original_url = const.ARTICLE_URL.format(content['id'])
    title = content['title']
    background_image = content['image_url']
    date = timer.timestamp_to_date(content['created'])
    author = content['author']['name']
    author_page = const.AUTHOR_PAGE_URL.format(content['author']['url_token'])
    avatar = content['author']['avatar_url']
    article_dict = {'author': author, 'author_avatar_url': avatar, 'author_page': author_page, 'title': title,
                    'original_url': original_url, 'created_date': date, 'background': background_image}
    return document.Meta(**article_dict)


def articles_id(column_id):
    article_list = list()
    offset = zhihu.Controller()
    while not offset.is_end():
        print(GET_ARTICLES_ID)
        response = net.column_spider(column_id, offset.next_offset())
        if response is None:
            raise ValueError('Response is None')
        content = response.text
        totals = re.search(r'"totals":\W(\d+)', content).group(1)
        offset.totals = int(totals)
        article_id_list = re.findall(r'"id":\W(\d+)', content)
        offset.increase(len(article_id_list))
        article_list.extend(article_id_list)
        article_id_list.clear()
        timer.random_sleep(end=zhihu.SLEEP)
    return article_list


def column_warehouse(column_id, warehouse):
    response = net.column_msg_spider(column_id)
    if response is not None:
        response_json = response.json()
        name = response_json['title']
        warehouse = os.path.join(warehouse, name)
        if not os.path.exists(warehouse):
            os.makedirs(warehouse)
        return warehouse
    else:
        raise ValueError('Response is None')


"""
说明：
    这里实现了单篇文章和专栏的爬取。
    article 根据article_id发起网络请求，返回的json文件中包含文章的基本信息和文章主体内容，解析文章的基本信息生成一个msg
字典对象，再将文章主体解析成BeautifulSoup对象，连同msg字典一起交给document模块下的Article解析并保存成markdown文件。
    根据专栏id获得专栏下的文章所有文章id后，逐一看成是单一的文章，由article爬取。
"""
