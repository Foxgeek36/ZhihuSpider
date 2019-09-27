import requests
from requests import HTTPError

from util.const import *
from .api import *

__all__ = ['article_spider_url', 'answer_spider', 'answers_spider', 'user_answers_spider', 'article_spider',
           'column_spider', 'user_articles_spider', 'user_column_spider', 'user_msg_spider', 'column_msg_spider',
           'question_msg_spider', 'article_spider', 'topic_essence_spider', 'topic_msg_spider', 'collection_msg_spider',
           'collection_spider']


def get(url, hearders):
    try:
        response = requests.get(url, headers=hearders, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.ReadTimeout as e:
        print('连接超时：', e)
    except requests.exceptions.ConnectionError as e:
        print('无法连接：', e)
    except HTTPError as e:
        print('连接错误：', e)
    return None


def get_html(url):
    return get(url, HTML_HEADERS)


def get_json(url):
    return get(url, JSON_HEADERS)


def answer_spider(answer_id):
    url = answer_api(answer_id)
    return get_json(url)


def answers_spider(question_id, offset, sort_by, limit=LIMIT_SIZE):
    url = all_answers_api(question_id, limit, offset, sort_by)
    return get_json(url)


def user_answers_spider(user_id, offset, sort_by, limit=LIMIT_SIZE):
    url = user_answers_api(user_id, limit, offset, sort_by)
    return get_json(url)


def article_spider(article_id):
    url = article_api(article_id)
    # 比较特殊，要用 get_html 方法
    return get_html(url)


def column_spider(column_id, offset, limit=LIMIT_SIZE):
    url = columns_article_api(column_id, limit, offset)
    # 比较特殊，要用 get_html 方法
    return get_html(url)


def user_articles_spider(user_id, offset, sort_by, limit=LIMIT_SIZE):
    url = user_articles_api(user_id, offset, limit, sort_by)
    return get_json(url)


def user_column_spider():
    pass


def user_msg_spider(user_id):
    url = user_msg_api(user_id)
    return get_json(url)


def column_msg_spider(column_id):
    url = columns_msg_api(column_id)
    return get_json(url)


def question_msg_spider(question_id):
    url = question_msg_api(question_id)
    return get_json(url)


def article_spider_url(article_id):
    return article_api(article_id)


def topic_essence_spider(topic_id, offset, limit=LIMIT_SIZE):
    url = topic_essence_api(topic_id, offset, limit)
    return get_json(url)


def topic_msg_spider(topic_id):
    url = topic_msg_api(topic_id)
    return get_json(url)


def collection_msg_spider(collection_id):
    url = collection_msg_api(collection_id)
    return get(url, COLLECTION_HEADERS)


def collection_spider(collection_id, page):
    url = collection_html_api(collection_id, page)
    return get_html(url)


"""
说明：
    这里定义了用于不同api的网络请求函数，函数统一返回response对象，如果发生网络请求错误会给出可能的错误类型，不会引发
错误。当出错时返回的是None。
"""
