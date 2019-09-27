import re

from bs4.element import NavigableString as HtmlStr
from bs4.element import Tag as HtmlTag

REFERENCE_LIST = []
EVENT_RECORD = None
RECORDING = False


class Simple:
    """
    设计理念：to_markdown() 完成元素的解析和编译功能，
    直接返回编译结果，不做保存（目前还不需要），仅保留以下函数
    """
    type = 'Simple'
    support: dict = {}

    def __init__(self, element_tag: HtmlTag = None):
        self.next_sibling = None
        self.element_tag = element_tag

    def to_markdown(self):
        """解析并返回 Tag 的 Markdown 形式"""
        return ''

    def element_type(self):
        """返回类的类型或者None"""
        return self.type

    def detail_type(self):
        """如果元素有细分的具体类型，就返回具体的类型，没有就返回类的类型"""
        return self.type

    def compile_for_quote(self):
        return ''

    def __str__(self):
        return self.type + str(self.element_tag)


class Code(Simple):
    type = 'code'
    tag_class = 'highlight'
    support = {'code', 'pre', 'div'}

    def __init__(self, element_tag: HtmlTag = None):
        super().__init__(element_tag)
        if self.element_tag.name == 'code':
            self.code = self.element_tag.get_text()
        else:
            self.language = 'text'
            if self.element_tag.name == 'div':
                code = self.element_tag.pre.prettify()
            else:
                code = self.element_tag.prettify()
            search_language = re.search(r'"language-(.+?)">', code)
            if search_language:
                self.language = re.sub(r'\d+', '', search_language.group(1))
            try:
                code = re.sub(r'(</span>)|(<span class=".+?">)', '', code)
                code = re.sub(r'(<pre><code class=".+?">)|(</code></pre>)', '', code)
                code = re.sub(r'&lt;', '<', code)
                code = re.sub(r'&amp;', '&', code)
                self.code = re.sub(r'&gt;', '>', code)
            except AttributeError:
                from util import timer
                file = timer.timestamp() + '.html'
                with open(file, 'w', encoding='utf8') as foo:
                    foo.write(self.element_tag.prettify())
                raise TypeError("can't find any code! %s" % file)

    def to_markdown(self):
        if self.element_tag.name == 'code':
            return ' `%s` ' % self.code
        else:
            return '```{}\n{}\n```'.format(self.language, self.code.strip())

    def compile_for_quote(self):
        md = self.to_markdown()
        codes = re.split(r'\n', md)
        code = ''
        for c in codes:
            code += '> ' + c + '\n'
        return code


class Figure(Simple):
    type = 'figure'

    def __init__(self, element_tag: HtmlTag = None):
        super().__init__(element_tag)
        img_attrs = self.element_tag.find('img').attrs
        img_selector = ['data-original', 'data-actualsrc', 'data-default-watermark-src', 'src']
        for img in img_selector:
            self.figure_link = img_attrs.get(img, None)
            if self.figure_link is not None:
                break
        describe_tag = self.element_tag.find('figcaption')
        self.describe = ''
        if describe_tag is not None:
            self.describe = describe_tag.get_text(strip=True)

    def to_markdown(self):
        return '![%s](%s "%s")' % (self.describe, self.figure_link, self.describe)


class Link(Simple):
    type = 'link'
    support = {'a': 'a', 'sup': 'sup'}

    def __init__(self, element_tag: HtmlTag = None):
        super().__init__(element_tag)
        if self.support.get(self.element_tag.name, '') == 'a':
            url = self.element_tag['href']
            if not bool(re.search(r'(http)|(www)', url)):
                url = 'https://www.zhihu.com' + url
            self.url = url
            text = self.element_tag.get_text('#', strip=True)
            self.text = re.sub(r'#.#', '——', text)
        else:
            self.text = self.element_tag['data-text'].strip()
            self.url = self.element_tag['data-url'].strip()

    def to_markdown(self):
        return '[%s](%s)' % (self.text, self.url)


class Url(Simple):
    type = 'a'


class Video(Simple):
    type = 'video'
    tag_class = 'video-box'
    not_video = 'not video type'

    def __init__(self, element_tag: HtmlTag):
        super().__init__(element_tag)
        self.video_link = self.element_tag.find('span', class_='url').get_text(strip=True)
        self.figure_link = self.element_tag.find('img', 'thumbnail')['src']
        title = self.element_tag.find('span', class_='title').get_text(strip=True)
        if title == '':
            title = '无题 '
        describe = '《%s》' % title
        self.video_title = describe

    def to_markdown(self):
        figure = '![%s](%s "%s")' % (self.video_title, self.figure_link, self.video_title)
        video_tip = '**%s，观看视频请访问** ：[%s](%s)' % (self.video_title, self.video_link, self.video_link)
        return figure + '\n' + video_tip


class Math(Simple):
    type = 'img'
    type_i = 'inline'
    type_b = 'block'

    def __init__(self, element_tag: HtmlTag):
        super().__init__(element_tag)
        self.img_url = self.element_tag['src'].strip()
        self.expression = self.element_tag['alt']

    def to_markdown(self, style=type_i):
        if style == self.type_i:
            return '$%s$' % self.expression
        else:
            return '$$\n%s\n$$' % self.expression

    def compile_for_quote(self, style=type_i):
        if style == Math.type_i:
            return '> $%s$' % self.expression
        else:
            return '> $$\n> %s\n> $$' % self.expression


class String(Simple):
    type = 'string'
    blank_type = 'ztext-empty-paragraph'
    not_empty = 'not empty'

    def __init__(self, element_tag: (HtmlStr, HtmlTag)):
        super().__init__(element_tag)
        self.text = self.element_tag.strip()

    def to_markdown(self):
        return self.text

    def detail_type(self):
        return super().detail_type()


class NewLine(Simple):
    type = 'br'

    def __init__(self, element_tag: HtmlTag):
        super().__init__(element_tag)
        self.text = '  \n'

    def to_markdown(self):
        return self.text


class Horizontal(Simple):
    type = 'hr'

    def __init__(self, element_tag: HtmlTag):
        super().__init__(element_tag)
        self.text = '---'

    def to_markdown(self):
        return self.text


class Unsupported(Simple):
    type = 'unsupported'

    def __init__(self, element_tag: HtmlTag):
        super().__init__(element_tag)
        self.text = '**不支持的标签：%s**' % self.element_tag.name

    def to_markdown(self):
        return self.text


class Superscript(Simple):
    type = 'sup'

    def __init__(self, element_tag: HtmlTag = None):
        super().__init__(element_tag)
        tag_attrs = self.element_tag.attrs
        self.text = self.element_tag.text.strip()
        self.url = tag_attrs['data-url']
        self.index = tag_attrs['data-numero']
        self.ref_text = tag_attrs['data-text']
        REFERENCE_LIST.append(self)

    def to_markdown(self):
        return '[%s](%s)' % (self.text, self.url)

    def to_reference(self):
        return self.index + '. ' + '[%s](%s)' % (self.ref_text, self.url)


"""
说明：
    Simple 类是基类（接口），parse模块下的所有类都直接或间接继承了Simple类。凡是直接继承了Simple类的类都是属于基本元素
类。既内容单一，不能再细分的元素。如图片类（figure）、视频类（Video）、代码类（Code），这些类都是可以直接解析成markdown
元素的基本元素。Multilevel类是所用复合类型的基类，这个基类也继承了Simple类。比如说一个p标签就是一个Paragraph类，p标签可
以含有a标签、b标签等，这些都属于是复合标签，也就是复合类型。理论上复合类型还可以相互嵌套，比较复杂，需要逐步向基本类型
分解。
"""
