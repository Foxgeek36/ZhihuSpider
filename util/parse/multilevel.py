from bs4.element import NavigableString as HtmlStr
from bs4.element import Tag as HtmlTag

from .simple import *

__all__ = ['Text']


class Multilevel(Simple):
    """
    实现理念：创建对象时解析，to_markdown() 时编译，
    免去了各种编译状态问题，也简化了实现逻辑
    就目前的功能实现还用不到多次 to_markdown() 的情景，
    编译结果直接返回给调用位置，不做保存
    """
    type = 'multilevel'
    support: dict = {}
    blank = ' '

    def __init__(self, element_tag: HtmlTag):
        super().__init__(element_tag)
        self.root = None
        self.probe = None
        head = Simple()
        probe = head
        for element in element_tag.children:
            if isinstance(element, HtmlStr):
                if len(element.strip()) != 0:
                    probe.next_sibling = String(element)
                    probe = probe.next_sibling
                continue
            element_tag_type = element.name
            # br 标签出现的频率特别高，放在第一位有利于提高程序效率
            if element_tag_type == NewLine.type:
                probe.next_sibling = NewLine(element)
            elif element_tag_type in Paragraph.support:
                if element.attrs.get('class', String.not_empty)[0] == String.blank_type:
                    continue
                else:
                    probe.next_sibling = Paragraph(element)
            elif element_tag_type in FontStyle.support:
                probe.next_sibling = FontStyle(element)
            elif element_tag_type == Url.type:
                try:
                    element_class = element.attrs.get('class', Video.not_video)[0]
                    probe.next_sibling = Video(element) if element_class == Video.tag_class else Link(element)
                except IndexError:
                    probe.next_sibling = Link(element)
            elif element_tag_type in Table.support:
                probe.next_sibling = Table(element)
            elif element_tag_type in Code.support:
                if element_tag_type == 'div':
                    element_class = element.attrs.get('class')[0]
                    probe.next_sibling = Code(element) if element_class == Code.tag_class else Paragraph(element)
                else:
                    probe.next_sibling = Code(element)
            else:
                probe.next_sibling = tag_dict.get(element_tag_type, Unsupported)(element)
            probe = probe.next_sibling
        self.root = head.next_sibling

    def to_markdown(self):
        """创建对象时解析，to_markdown() 时编译"""
        return super().to_markdown()

    @staticmethod
    def add_blank(element: Simple):
        """判断编译时是否需要在兄弟标签的编译内容首尾添加空格"""

        if element.next_sibling is not None:
            return element.detail_type() in [Link.type, *FontStyle.format_type, Unsupported.type, Superscript.type]
        else:
            return False

    def __len__(self):
        probe = self.root
        length = 0
        while probe is not None:
            length += 1
            probe = probe.next_sibling
        return length

    def __next__(self):
        # 联合 __iter__ 函数，令其初始化指针 self.probe
        # 这里只要 probe 不是 None 就返回其指向的数据，否则就引发停止迭代
        # 引发停止迭代时不需要让指针指向 self.root，__iter__ 会在下次被调用时将其初始化
        if self.probe is None:
            raise StopIteration
        item = self.probe
        self.probe = self.probe.next_sibling
        return item

    def __iter__(self):
        self.probe = self.root
        return self

    def detail_type(self):
        return super().detail_type()


class Text(Multilevel):
    type = 'text'

    def __init__(self, element_tag: HtmlTag):
        super().__init__(element_tag)

    def to_markdown(self):
        text = ''
        for paragraph in self:
            if isinstance(paragraph, Math):
                para = paragraph.to_markdown(Math.type_b)
            else:
                para = paragraph.to_markdown()
            if para != '':
                text += para + '\n\n'
        ref_text = ''
        if len(REFERENCE_LIST) != 0:
            ref_text = '**参考文献**：\n\n'
            for ref in REFERENCE_LIST:
                ref_text += ref.to_reference() + '\n'
        return text + ref_text


class Paragraph(Multilevel):
    type = 'paragraph'
    support: dict = {'p': 'p', 'span': 'span'}

    def __init__(self, element_tag: HtmlTag):
        super().__init__(element_tag)
        # if '模2运算中两个相同的数相加为' in self.element_tag.prettify():
        #     print('__init__:', self.element_tag)

    def to_markdown(self):
        paragraph = ''
        for sentence in self:
            if isinstance(sentence, Math) and len(self) == 1:
                sent = ' {} '.format(sentence.to_markdown(Math.type_b))
            else:
                sent = sentence.to_markdown()
                if self.add_blank(sentence):
                    sent = ' {} '.format(sent)
            paragraph += sent
        return paragraph

    def compile_for_quote(self):
        if len(self) == 1 and isinstance(self.root, Math):
            return self.root.compile_for_quote(style=Math.type_b)
        else:
            return self.to_markdown()


class Quote(Multilevel):
    type = 'blockquote'
    support = {'blockquote'}

    def __init__(self, element_tag: HtmlTag):
        super().__init__(element_tag)

    def to_markdown(self):
        sentences = list()
        sentence = ''
        for quote in self:
            if isinstance(quote, NewLine):
                if sentence != '':
                    sentences.append('> ' + sentence + '  \n')
                    sentence = ''
            elif isinstance(quote, Paragraph):
                if sentence != '':
                    sentences.append('> ' + sentence + '  \n')
                sentences.append('> ' + quote.to_markdown() + '  \n')
                sentence = ''
            elif isinstance(quote, Code) or isinstance(quote, Table) or isinstance(quote, Math):
                if sentence != '':
                    sentences.append('> ' + sentence + '  \n')
                sentences.append(quote.compile_for_quote())
                sentence = ''
            else:
                q = quote.to_markdown()
                if self.add_blank(quote):
                    q += ' '
                sentence += q
        if sentence != '':
            sentences.append('> ' + sentence + '  \n')
        return ''.join(sentences)


class Table(Multilevel):
    type = 'table'
    type_ul = 'ul'
    type_ol = 'ol'
    support = {'ul': 'ul', 'ol': 'ol'}

    def __init__(self, element_tag: HtmlTag):
        super().__init__(element_tag)
        self.index = 0

    def to_markdown(self):
        table_md = ''
        for li in self:
            li_md = li.to_markdown()
            table_md += self.get_index() + li_md.strip() + '\n'
        return table_md

    def get_index(self):
        if self.support.get(self.element_tag.name, '') == 'ol':
            self.index += 1
            return str(self.index) + '. '
        return '- '

    def compile_for_quote(self):
        table_md = ''
        for li in self:
            li_md = li.to_markdown()
            table_md += '> ' + self.get_index() + li_md.strip() + '  \n'
        return table_md


class FontStyle(Multilevel):
    type = 'font_style'
    support: dict = {'h1': 'h1', 'h2': 'h2', 'h3': 'h3', 'h4': 'h4', 'h5': 'h5', 'h6': 'h6',
                     'em': 'em', 'strong': 'strong', 'b': 'b', 'i': 'i', 'u': 'u', 'li': 'li'}
    plus_type = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'u', 'li'}
    plus_span = {'h1': '# ', 'h2': '## ', 'h3': '### ', 'h4': '#### ', 'h5': '##### ', 'h6': '###### ',
                 'u': '', 'li': ''}
    format_type = {'em', 'strong', 'b', 'i'}
    format_span = {'em': '**{}**', 'strong': '**{}**', 'b': '**{}**', 'i': '*{}*'}

    def __init__(self, element_tag: HtmlTag):
        super().__init__(element_tag)

    def to_markdown(self):
        paragraph = ''
        for sentence in self:
            sent = sentence.to_markdown()
            if self.add_blank(sentence):
                sent += ' {} '.format(sent)
            paragraph += sent
        if self.detail_type() in self.plus_type:
            md = self.plus_span.get(self.detail_type(), '') + paragraph
        else:
            md = self.format_span.get(self.detail_type(), '{}').format(paragraph)
        return md

    def detail_type(self):
        return self.support.get(self.element_tag.name, '')


# 这个字典应用于 Multilevel 中的构造函数，不宜随意修改！
tag_dict = {Quote.type: Quote, Figure.type: Figure, Math.type: Math,
            NewLine.type: NewLine, Horizontal.type: Horizontal, Superscript.type: Superscript}

"""
说明：
    这里实现的都是复合类型，需要进一步向基础类型解析，不同的复合类型之间还有比较大的区别。Text是整篇文章的主体，由它向下
解析生成段，段再向下解析生成各种类。最复杂的应该是Quote类，因为引用标签只是提供了一个引用环境，可以嵌套很多种类型的标签。
"""
