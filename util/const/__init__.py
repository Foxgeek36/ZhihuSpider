JSON_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
                "Host": "www.zhihu.com",
                "Referer": "https://www.zhihu.com/"}

USER_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
                'authority': 'www.zhihu.com',
                "Referer": ""}


def get_user_headers(user_id):
    ref = r'https://www.zhihu.com/people/{}/posts'
    USER_HEADERS['Referer'] = ref.format(user_id)
    return USER_HEADERS


HTML_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
                'authority': 'zhuanlan.zhihu.com'}

COLLECTION_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                                    '(KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
                      'authority': 'api.zhihu.com'}

SORT_BY_DEF = 'default'
SORT_BY_VOT = 'voteups'
SORT_BY_DAT = 'created'
PLATFORM = 'desktop'

# 作者头像
AVATAR_SIZE_R = '{size}'
AVATAR_SIZE_A = 'l'  # is L
# size: r, m, b, l, xs, is, s

# 作者主页 format(url_token)
AUTHOR_PAGE_URL = 'https://www.zhihu.com/people/{}'

# 答案原文链接 format: question_id, answer_id
# 没有考虑到 question_id，先前爬取的答案原文链接都不对    2019-05-02 更正
ANSWER_URL = r'https://www.zhihu.com/question/{}/answer/{}'

# 文章原文链接
ARTICLE_URL = 'https://zhuanlan.zhihu.com/p/{}'

# 设置休眠时长（秒）
TIME_SLEEP = 6

LIMITLESS = -1

LIMIT_SIZE = 20  # 每次获取答案的数量

