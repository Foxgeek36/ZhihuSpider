import os
import re

from bs4.element import Tag as HtmlTag

from util.parse.multilevel import Text

__all__ = ['Article', 'Answer']

""" document 利用传入的文章头字典信息和解析的文章体合成一篇文章，文章体的解析由 parse 模块来承担"""


class Meta:
    def __init__(self, author: str = None, author_avatar_url: str = None, author_page: str = None,
                 title: str = None, original_url: str = None, created_date: str = None, voteup: int = None,
                 background: str = None):
        self.author = author
        self.author_avatar_url = author_avatar_url
        self.author_page = author_page
        self.title = title
        self.original_url = original_url
        self.created_date = created_date
        self.voteup = voteup
        self.background = background


class BaseArticle:
    def __init__(self, tag, meta: Meta):
        self.author = meta.author
        self.author_avatar_url = meta.author_avatar_url
        self.author_page = meta.author_page
        self.title = meta.title
        self.original_url = meta.original_url
        self.created_date = meta.created_date
        self.voteup = meta.voteup
        self.background = meta.background
        self.file_name = ''
        self.text = Text(tag)
        self.markdown = self.compile()

    def get_file_name(self, template):
        """%v-%d-%a-%t"""
        title = re.sub(r'[\\/]', '、', self.title)
        title = re.sub(r'[？?*:<>"|\n\t]', '', title)
        date = re.sub(r'-', '', self.created_date)
        file_name_split = {'%a': self.author, '%d': date, '%t': title, '%v': str(self.voteup)}
        file_name_t = template.split('-')
        names = []
        for te in file_name_t:
            e = file_name_split.get(te, '')
            names.append(e)
        name = '-'.join(names)
        return name + '.md'

    def make_markdown(self, path):
        file = os.path.join(path, self.file_name)
        foo = open(file, 'w', encoding='utf-8')
        foo.write(self.markdown)
        foo.close()

    def compile(self):
        return ''

    def to_markdown(self):
        return self.markdown

    def __iter__(self):
        return iter(self.text)

    def set_file_name(self, template=None, file_name=None):
        if template is not None:
            self.file_name = self.get_file_name(template)
        elif file_name is not None:
            self.file_name = file_name
        else:
            raise ValueError


class Answer(BaseArticle):
    def __init__(self, answer_tag: HtmlTag, meta: Meta):
        super(Answer, self).__init__(answer_tag, meta)
        if not isinstance(answer_tag, HtmlTag):
            raise TypeError('answer_tag except a HtmlTag type, not %s' % type(answer_tag))
        self.file_name = self.get_file_name('%a-%t-<%v>')

    def compile(self):
        title = '# [%s](%s)\n\n' % (self.title, self.original_url)
        split_line = '-' * len(title) + '\n\n'
        head_img = '![%s](%s "%s")&emsp;' % (self.author, self.author_avatar_url, self.author)
        author = '**[%s](%s) / %s**  👍 %d\n\n' % (
            self.author, self.author_page, self.created_date, self.voteup)
        markdown_head = title + split_line + head_img + author
        return markdown_head + self.text.to_markdown()

    def answer_msg(self):
        return '%s    %s / %s  👍 %d' % (self.title, self.author, self.created_date, self.voteup)

    def __str__(self):
        return '%s\n%s / %s 👍 %d' % (self.title, self.author, self.created_date, self.voteup)


class Article(BaseArticle):
    def __init__(self, article_tag: HtmlTag, meta: Meta):
        super(Article, self).__init__(article_tag, meta)
        if not isinstance(article_tag, HtmlTag):
            raise TypeError('answer_tag except a HtmlTag type, not %s' % type(article_tag))
        self.file_name = self.get_file_name('%t')

    def compile(self):
        background = ''
        if self.background is not None and self.background != '':
            background = '![背景大图](%s)\n\n' % self.background
        title = '# [%s](%s)\n\n' % (self.title, self.original_url)
        split_line = '-' * len(title) + '\n\n'
        head_img = '![%s](%s "%s")&emsp;' % (self.author, self.author_avatar_url, self.author)
        author = '**[%s](%s) / %s**\n\n' % (
            self.author, self.author_page, self.created_date)
        markdown_head = background + title + split_line + head_img + author
        return markdown_head + self.text.to_markdown()

    def article_msg(self):
        return '%s     %s / %s' % (self.title, self.author, self.created_date)

    def __str__(self):
        return '%s\n%s / %s' % (self.title, self.author, self.created_date)


"""
说明：
    document模块统一了文章、问答的markdown生成样式，两者的区别仅在于：文章类有背景大图，问答类有点赞数。
    这两个模块接收内容主体的基本信息和内容主体，解析基本信息并编译成文章头。内容主体由parse模块下的Text类解析成markdown
形式并返回给这里的调用者。最后模块将文章头和主体合成一篇markdown文档，由外部提供保存路径保存到本地硬盘。
"""
