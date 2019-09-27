import os
import re
from util import net
from bs4 import BeautifulSoup
from util import document
from util import const
from util.timer import timer
from json.decoder import JSONDecodeError
import zhihu


def topic_essence(topic_id, warehouse):
    """获取并解析精华内容，根据内容的类型向 essence_answer，essence_article 分流"""
    offset = zhihu.Controller(crawl_times=200, limit=10)  # 需要写一个新的控制器
    warehouse = topic_warehouse(topic_id, warehouse)
    while not offset.is_end():
        response = net.topic_essence_spider(topic_id, offset.next_offset())
        if response is None:
            raise ValueError('Response is None')
        try:
            response_json = response.json()
            database: list = response_json['data']
            offset.running_status(response_json['paging']['is_end'])
            offset.increase(len(database))
            for content in database:
                if content['target']['type'] == 'answer':
                    essence_answer(content['target'], warehouse)
                elif content['target']['type'] == 'article':
                    essence_article(content['target'], warehouse)
        except JSONDecodeError as e:
            raise e
        timer.sleep_for(zhihu.SLEEP)
    print(offset)


def essence_answer(content, warehouse):
    """获取必要的 msg_dict 信息封装成一个 Answer 对象，并生成 markdown 文件"""
    author = content['author']['name']
    avatar = content['author']['avatar_url_template'].replace(const.AVATAR_SIZE_R,
                                                              const.AVATAR_SIZE_A)
    author_page = const.AUTHOR_PAGE_URL.format(content['author']['url_token'])
    title = content['question']['title']
    question_id = content['question']['id']
    answer_id = content['id']
    original_url = const.ANSWER_URL.format(question_id, answer_id)
    date = timer.timestamp_to_date(content['created_time'])
    voteup = content['voteup_count']
    msg_dict = {'author': author, 'author_avatar_url': avatar, 'author_page': author_page, 'title': title,
                'original_url': original_url, 'created_date': date, 'voteup': voteup}
    answer_content = BeautifulSoup(content['content'], 'lxml').body
    answer = document.Answer(answer_content, msg_dict)
    answer.make_markdown(warehouse)
    print(answer.answer_msg())


def essence_article(content, warehouse):
    """获取必要的 msg_dict 信息封装成一个 Article 对象，并生成 markdown 文件"""
    author = content['author']['name']
    avatar = content['author']['avatar_url_template'].replace(const.AVATAR_SIZE_R,
                                                              const.AVATAR_SIZE_A)
    author_page = const.AUTHOR_PAGE_URL.format(content['author']['url_token'])
    title = content['title']
    original_url = content['url']
    date = timer.timestamp_to_date(content['created'])
    try:
        # 有些文章没有背景大图，需要做空白处理
        background = re.sub(r'[^_]+?(?=.jpg)', 'r', content['image_url'])
    except KeyError:
        background = ''
    msg_dict = {'author': author, 'author_avatar_url': avatar, 'author_page': author_page, 'title': title,
                'original_url': original_url, 'created_date': date, 'background': background}
    article_content = BeautifulSoup(content['content'], 'lxml').body
    article = document.Article(article_content, msg_dict)
    article.make_markdown(warehouse)
    print(article.article_msg())


def topic_warehouse(topic_id, warehouse):
    response = net.topic_msg_spider(topic_id)
    if response is not None:
        response_json = response.json()
        name = response_json['name']
        name = re.sub(r'[\\/]', '、', name)
        name = re.sub(r'[？?*:<>|]', '', name)
        warehouse = os.path.join(warehouse, name)
        if not os.path.exists(warehouse):
            os.makedirs(warehouse)
        return warehouse
    else:
        raise ValueError('Response is None')


"""
说明；
    这个模块的函数有注释，查看有关注释即可.

"""
