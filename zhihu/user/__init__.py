import os
import re
from json.decoder import JSONDecodeError

from bs4 import BeautifulSoup

import zhihu
from util import const
from util import document
from util import net
from util import timer

__all__ = ['user_answers', 'user_articles']

user_msg_dict = {'name': '',
                 'avatar_url': '',
                 'url': ''}


def user_answers(user_id, warehouse):
    init_user_msg(user_id)
    offset = zhihu.Controller()
    while not offset.is_end():
        response = net.user_answers_spider(user_id, offset.next_offset(), const.SORT_BY_DAT)
        if response is None:
            raise ValueError('Response is None')
        try:
            response_json = response.json()
            offset.totals = response_json['paging']['totals']
            database: list = response_json['data']
            offset.increase(len(database))
            for answer_content in database:
                msg = answer_msg(answer_content)
                content = BeautifulSoup(answer_content['content'], 'lxml').body
                an = document.Answer(content, msg)
                an.make_markdown(warehouse)
                print(an.answer_msg())
            timer.sleep_for(zhihu.SLEEP)
        except JSONDecodeError as e:
            raise e


def user_articles(user_id, warehouse):
    init_user_msg(user_id)
    offset = zhihu.Controller()
    warehouse = get_warehouse(user_id, warehouse)
    while not offset.is_end():
        response = net.user_articles_spider(user_id, offset.next_offset(), const.SORT_BY_DAT)
        if response is None:
            raise ValueError('Response is None')
        try:
            response_json = response.json()
            offset.totals = response_json['paging']['totals']
            database: list = response_json['data']
            offset.increase(len(database))
            for article_content in database:
                msg = article_msg(article_content)
                content = BeautifulSoup(article_content['content'], 'lxml').body
                ar = document.Article(content, msg)
                ar.make_markdown(warehouse)
                print(ar.article_msg())
            timer.sleep_for(zhihu.SLEEP)
        except JSONDecodeError as e:
            raise e


def answer_msg(content):
    voteup = content['voteup_count']
    title = content['question']['title']
    question_id = content['question']['id']
    answer_id = content['id']
    original_url = const.ANSWER_URL.format(question_id, answer_id)
    date = timer.timestamp_to_date(content['created_time'])
    answer_dict = {'author': user_msg_dict['name'], 'author_avatar_url': user_msg_dict['author_avatar_url'],
                   'author_page': user_msg_dict['author_page'], 'title': title,
                   'original_url': original_url, 'created_date': date, 'voteup': voteup}
    return answer_dict


def article_msg(content):
    original_url = content['url']
    title = content['title']
    background_image = content['image_url']
    date = timer.timestamp_to_date(content['created'])
    article_dict = {'author': user_msg_dict['name'], 'author_avatar_url': user_msg_dict['author_avatar_url'],
                    'author_page': user_msg_dict['author_page'], 'title': title,
                    'original_url': original_url, 'created_date': date, 'background': background_image}
    return document.Meta(**article_dict)


def init_user_msg(user_id):
    response = net.user_msg_spider(user_id)
    if response is None:
        raise ValueError('Response is None')
    else:
        response_json = response.json()
        user_msg_dict['name'] = response_json['name']
        user_msg_dict['author_page'] = response_json['url']
        user_msg_dict['author_avatar_url'] = response_json['avatar_url_template'].replace(const.AVATAR_SIZE_R,
                                                                                          const.AVATAR_SIZE_A)


def get_warehouse(user_id, warehouse):
    response = net.user_msg_spider(user_id)
    if response is None:
        raise ValueError('Response is None')
    else:
        response_json = response.json()
        name = response_json['name']
        name = re.sub(r'[/\\:*?"<>|]', '', name)
        warehouse = os.path.join(warehouse, name)
        if not os.path.exists(warehouse):
            os.makedirs(warehouse)
        return warehouse


"""
说明：
    通过用户id发起网络请求，返回的json文件中包含需要的所有信息，解析相应的信息交给document模块下的有关类处理生成
markdown文件即可
"""
