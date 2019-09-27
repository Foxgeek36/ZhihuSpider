import os
import re
from json.decoder import JSONDecodeError

from bs4 import BeautifulSoup

import zhihu
from util import const
from util import document
from util import net
from util.timer import timer

__all__ = ['answer', 'answers', 'make_answers_as_book']

template = '''
{} {}    {} / {}  👍 {}
    {}
    评分：{:<.2f}
    收录：{}
'''


def answer(answer_id, warehouse):
    response = net.answer_spider(answer_id)
    if response is not None:
        answer_content = response.json()
        content = BeautifulSoup(answer_content['content'], 'lxml').body
        # # TODO DEBUG TAG CLEAR AFTER FINISH!
        # with open(answer_id + '.html', 'w', encoding='utf8') as foo:
        #     foo.write(content.prettify())
        msg = answer_msg(answer_content)
        an = document.Answer(content, msg)
        an.make_markdown(warehouse)
        return an.answer_msg()
    else:
        raise ValueError('Response is None')


def answers(question_id, warehouse):
    offset = zhihu.Controller()
    warehouse = question_warehouse(question_id, warehouse)
    while not offset.is_end():
        response = net.answers_spider(question_id, offset.next_offset(), const.SORT_BY_VOT)
        if response is None:
            raise ValueError('Response is None')
        try:
            response_json = response.json()
            offset.totals = response_json['paging']['totals']
            database: list = response_json['data']
            offset.increase(len(database))
            for answer_content in database:
                msg = answer_msg(answer_content)
                if not offset.to_collect(answer_content):
                    continue
                content = BeautifulSoup(answer_content['content'], 'lxml').body
                an = document.Answer(content, msg)
                an.set_file_name(template='%a-%v')
                an.make_markdown(warehouse)
                print(an.answer_msg())
            timer.sleep_for(zhihu.SLEEP)
        except JSONDecodeError as e:
            raise e


def answer_msg(answer_content):
    author = answer_content['author']['name']
    voteup = answer_content['voteup_count']
    title = answer_content['question']['title']
    question_id = answer_content['question']['id']
    answer_id = answer_content['id']
    original_url = const.ANSWER_URL.format(question_id, answer_id)
    author_page = const.AUTHOR_PAGE_URL.format(answer_content['author']['url_token'])
    avatar = answer_content['author']['avatar_url_template'].replace(const.AVATAR_SIZE_R,
                                                                     const.AVATAR_SIZE_A)
    date = timer.timestamp_to_date(answer_content['created_time'])
    answer_dict = {'author': author, 'author_avatar_url': avatar, 'author_page': author_page, 'title': title,
                   'original_url': original_url, 'created_date': date, 'voteup': voteup}
    return document.Meta(**answer_dict)


def question_warehouse(question_id, warehouse):
    response = net.question_msg_spider(question_id)
    if response is not None:
        response_json = response.json()
        name = response_json['title']
        name = re.sub(r'[\\/]', '、', name)
        name = re.sub(r'[？?*:<>|]', '', name)
        warehouse = os.path.join(warehouse, name)
        if not os.path.exists(warehouse):
            os.makedirs(warehouse)
        return warehouse
    else:
        raise ValueError('Response is None')


def make_answers_as_book(question_id, warehouse):
    offset = zhihu.Controller()
    response = net.question_msg_spider(question_id)
    if response is not None:
        response_json = response.json()
        name = response_json['title']
        name = re.sub(r'[\\/]', '、', name)
        title = re.sub(r'[？?*:<>|]', '', name)
    else:
        raise ValueError('Response is None')
    book = open(os.path.join(warehouse, title + '.md'), 'a', encoding='utf8')
    while not offset.is_end():
        response = net.answers_spider(question_id, offset.next_offset(), const.SORT_BY_VOT)
        if response is None:
            raise ValueError('Response is None')
        try:
            response_json = response.json()
            offset.totals = response_json['paging']['totals']
            database: list = response_json['data']
            offset.increase(len(database))
            for answer_content in database:
                msg = answer_msg(answer_content)
                if not offset.to_collect(answer_content):
                    continue
                content = BeautifulSoup(answer_content['content'], 'lxml').body
                an = document.Answer(content, msg)
                an.set_file_name(template='%a-%v')
                book.write(an.to_markdown())
                book.write('\n---\n')
                print(an.answer_msg())
            timer.sleep_for(zhihu.SLEEP)
        except JSONDecodeError as e:
            book.close()
            os.remove(os.path.join(warehouse, title + '.md'))
            raise e
    book.close()


"""
说明：
    这里实现了对单个回答或问题的所有回答的爬取，其中单个回答的爬取需要的是answer_id，而问题的所有回答需要的是
question_id。通过相应的id发起网络请求，返回的json文件中包含的内容的主体，通过解析json文件获得文章的基本信息，生
成一个msg对象，再将内容主体解析成BeautifulSoup对象，连同msg一起交给document下的有关类解析生成markdown文件
"""
