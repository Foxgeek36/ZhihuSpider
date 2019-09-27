"""
API 没有包含全面的信息（user_id, limit, offset, sort_by），不能直接使用，需要编写索取函数，
利用索取函数完善 API 信息并返回完整、可用的API
这些 API 都不是原始的 API，有轻微删改，需要具体参考 API.md 文件（这个文件不能修改！），有些 API 还没有编写索取函数

    SORT_BY_DEF = 'default'
    SORT_BY_VOT = 'voteups'
    SORT_BY_DAT = 'created'
    PLATFORM = 'desktop'

这几个参数是在使用浏览器访问知乎的过程中发现的，关于排序似乎没有绝对的作用（比如按点赞数排序，而得到的数据总体有序，
局部排序不严格）
"""

__all__ = ['all_answers_api', 'answer_api', 'user_mark_answers_api', 'user_answers_api', 'user_questions_api',
           'user_pins_api', 'user_columns_api', 'columns_msg_api', 'columns_article_api', 'user_favlists_api',
           'collection_msg_api', 'collection_short_article_api', 'user_articles_api', 'user_msg_api', 'article_api',
           'question_msg_api', 'topic_essence_api', 'topic_msg_api', 'collection_html_api']

# 获得问题下的所有答案
# 将question替换为question.detail后, 即可获得问题描述数据
# format: question_id, limit, offset, sort_by
A_AS_API = 'https://www.zhihu.com/api/v4/questions/{}/answers?' \
           'include=data[*].voteup_count,content&limit={}&offset={}&sort_by={}'


def all_answers_api(question_id: str, limit: int, offset: int, sort_by: str):
    return A_AS_API.format(question_id, limit, offset, sort_by)


# 获得由 answer_id 指定的回答
# format: answer_id
ANSWER_API = 'https://www.zhihu.com/api/v4/answers/{}?include=data[*].voteup_count,content'


def answer_api(answer_id):
    return ANSWER_API.format(answer_id)


# 获得用户被收录的回答
# format: user_id, limit, offset, sort_by
USER_MA_AS_API = 'https://www.zhihu.com/api/v4/members/{}/marked-answers?' \
                 'include=data[*].content,voteup_count,created_time,updated_time,question,' \
                 '&limit={}&offset={}&sort_by={}'


def user_mark_answers_api(user_id: str, limit: int, offset: int, sort_by: str):
    return USER_MA_AS_API.format(user_id, limit, offset, sort_by)


# 获得用户按时间、点赞数排序的回答
# format: user_id, limit, offset, sort_by
USER_AS_API = 'https://www.zhihu.com/api/v4/members/{}/answers?' \
              'include=data[*].content,voteup_count,created_time,updated_time,question' \
              '&limit={}&offset={}&sort_by={}'


def user_answers_api(user_id: str, limit: int, offset: int, sort_by: str):
    return USER_AS_API.format(user_id, limit, offset, sort_by)


# 获得用户提出的问题
# 包含作者信息、问题标题、id、关注数、回答数、创建、更新时间、问题 url
# format: user_id, limit, offset
USER_QS_API = 'https://www.zhihu.com/api/v4/members/{}/questions?' \
              'include=data[*].created,answer_count,author&limit={}&offset={}'


def user_questions_api(user_id: str, limit: int, offset: int):
    return USER_QS_API.format(user_id, limit, offset)


# 获得用户的想法
# 包含作者信息、想法内容，想法配图等内容
# format: user_id, offset, limit
USER_PS_API = 'https://www.zhihu.com/api/v4/members/{}/pins?offset={}&limit={}'


def user_pins_api(user_id, offset, limit):
    return USER_PS_API.format(user_id, offset, limit)


# 获得用户的专栏
# 包含专栏的信息，id、名称、文章数量、作者信息等
# format: user_id, offset, limit
USER_CC_API = 'https://www.zhihu.com/api/v4/members/{}/column-contributions?' \
              'include=data[*].column.intro,articles_count&offset={}&limit={}'


def user_columns_api(user_id, offset, limit):
    return USER_CC_API.format(user_id, offset, limit)


# 获得有关专栏的信息
# 包含专栏 id， 专栏名称， 专栏文章数量， 专栏作者等信息
# format: column_id
CC_MSG_API = 'https://www.zhihu.com/api/v4/columns/{}?include=title,articles_count'


def columns_msg_api(column_id):
    return CC_MSG_API.format(column_id)


# 获得专栏下的文章信息
# 专栏下文章的 id，标题，背景图 url， 点赞数，发表、更新时间， 评论数， 作者个人信息
# 不包含文章的具体内容，需要根据文章 id 获得文章内容
# 获得文章 id 后按单篇的文章处理
# format: column_id, limit, offset
CC_ARTICLE_API = 'https://zhuanlan.zhihu.com/api/columns/{}/articles?' \
                 'include=data[*].voteup_count&limit={}&offset={}'


def columns_article_api(column_id, limit, offset):
    return CC_ARTICLE_API.format(column_id, limit, offset)


# 获得用户的收藏夹
# 获得收藏夹的名称、id、包含内容的数量(answer_count)
# 通过 id 构造 url 获得收藏的具体内容，内容包含在 html 源码中 每页 10 条
# 可根据 answer_count 计算页码，第一页可以不带页码
# https://www.zhihu.com/collection/158014176?page=3
# format: user_id, offset, limit
USER_FS_API = 'https://www.zhihu.com/api/v4/members/{}/favlists?&offset={}&limit={}'


def user_favlists_api(user_id, offset, limit):
    return USER_FS_API.format(user_id, offset, limit)


# 获得收藏夹的信息
# 包含创建者信息、收藏夹名称、创建时间、关注人数等信息
# format: collection_id
CO_MSG_API = 'https://api.zhihu.com/collections/{}'


def collection_msg_api(c_id):
    return CO_MSG_API.format(c_id)


# 获得收藏夹的html内容
# format: collection_id, page
COLLECTION_HTML_API = 'https://www.zhihu.com/collection/{}?page={}'


def collection_html_api(collection_id, page):
    return COLLECTION_HTML_API.format(collection_id, page)


# 获得收藏夹简短的内容（只包含答案部分，不包含文章）
# answers 改为 contents 也可以
# format: collection_id
CO_SA_API = 'https://api.zhihu.com/collections/{}/answers'


def collection_short_article_api(c_id):
    return CO_SA_API.format(c_id)


# 用户按时间、点赞数排序的文章
# 包含文章的具体内容，创建、更新时间，点赞数，url，标题，背景图 url，评论数等；还有作者个人信息
# format: user_id, offset, limit, sort_by
USER_AR_API = 'https://www.zhihu.com/api/v4/members/{}/articles?' \
              'include=data[*].content,voteup_count,created;&offset={}&limit={}&sort_by={}'


def user_articles_api(user_id, offset, limit, sort_by):
    return USER_AR_API.format(user_id, offset, limit, sort_by)


# 作者个人公开的基本信息
USER_MSG_API = 'https://www.zhihu.com/api/v4/members/{}?include=allow_message'


def user_msg_api(user_id):
    return USER_MSG_API.format(user_id)


# 根据文章 id 获得文章的具体内容
# https://api.zhihu.com/articles/66900790
# https://www.zhihu.com/api/v4/articles/66900790?include=title
# https://www.zhihu.com/api/v4/articles/66900790
# 以上三个 API 都可以获得基于 json 文件的文章内容（基本信息、主体），其中第一个 API 包含在返回的 json 文件中
# 下面这个 API 获得的文章内容是基于 html 的，源码中有具体的内容，也可以在 html 的 script 标签中提取基于 json 的文章内容
# https://zhuanlan.zhihu.com/p/66900790
# format: article_id
ARTICLE_API = 'https://api.zhihu.com/articles/{}'


def article_api(article_id):
    return ARTICLE_API.format(article_id)


# 问题信息
# 获得问题的标题、id、url, 创建、更新时间
# format: question_id
# 获得问题属性（题干，创建时间……） API
# format: question_id
# QUESTION_API = r'https://www.zhihu.com/api/v4/questions/{}'
QS_MSG_API = r'https://www.zhihu.com/api/v4/questions/{}?include=title'


def question_msg_api(question_id):
    return QS_MSG_API.format(question_id)


# 知乎话题
TOPIC_API = 'https://www.zhihu.com/api/v4/topics/{tid}'

# 话题-精华 API
# 获得话题下的精华模块内容（文章、回答），包含具体的内容，作者信息等
# format: topic_id, limit, offset
TOPIC_ESS_API = 'https://www.zhihu.com/api/v4/topics/{}/feeds/essence?' \
                'include=data[*].target.content;&limit={}&offset={}'


def topic_essence_api(topic_id, offset, limit):
    return TOPIC_ESS_API.format(topic_id, limit, offset)


# 话题信息API
# 获得话题的有关信息，其中包含 话题名称、id、url、简介
# https://www.zhihu.com/api/v4/topics/19740929/intro?include=content.meta.content.photos  可以得到更详细的信息
# format: topic_id
TOPIC_MSG_API = 'https://www.zhihu.com/api/v4/topics/{}'


def topic_msg_api(topic_id):
    return TOPIC_MSG_API.format(topic_id)


# https://www.zhihu.com/api/v4/members/xiao-gui-55-68/relations/mutuals?
# include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2C
# is_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=10

# 热搜关键词
# https://www.zhihu.com/api/v4/search/preset_words?w=

# 热门收藏
# https://www.zhihu.com/node/ExploreHotFavlistsInnerV2?params=%7B%22offset%22%3A2%7D


# 以下 API 使用 __all__.append() 加入到 __all__ 列表

# 获得回答下的评论
# 内容包含：作者，评论内容，子评论（列表），子评论作者，子评论被回复人，子评论内容
# format: answer_id
ANSWER_COMMENT_API = 'https://www.zhihu.com/api/v4/answers/{}/root_comments?' \
                     'order=normal&limit=20&offset=0&status=open'


def answer_comment_api(answer_id):
    return ANSWER_COMMENT_API.format(answer_id)


__all__.append('answer_comment_api')
