# -*- coding: utf-8 -*-
# @Time : 2021/11/19 0:50
# @Author : nefu-ljw
# @File : upload-markdown-to-wordpress.py
# @Function: Upload new posts in WordPress with local Markdown files
# @Software: PyCharm
# @Reference: original


import os  # 用来遍历文件路径
import frontmatter
import markdown
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from xml.etree.ElementTree import Element
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.util import AtomicString
import re
from markdown import Markdown


def _wrap_node(node, preview_text, wrapper_tag):
    preview = Element('span', {'class': 'MathJax_Preview'})
    preview.text = AtomicString(preview_text)
    wrapper = Element(wrapper_tag)
    wrapper.extend([preview, node])
    return wrapper


class InlineMathPattern(InlineProcessor):
    def handleMatch(self, m, data):
        node = Element('span')  # Use <span> instead of <p>
        node.text = AtomicString(m.group(0))  # Preserve $ symbols and math content
        return node, m.start(0), m.end(0)


class DisplayMathPattern(InlineProcessor):
    def handleMatch(self, m, data):
        node = Element('span')  # Retain <p> for display math as requested
        if '\\begin' in m.group(1):
            node.text = AtomicString(m.group(0))  # Content for \begin...\end blocks
        else:
            node.text = AtomicString(m.group(0))  # Content for $$...$$ or $$...$$
        return node, m.start(0), m.end(0)


class GitLabPreprocessor(Preprocessor):
    """
    Preprocessor for GitLab-style standalone syntax:

    ```math
    math goes here
    ```
    """

    def run(self, lines):
        inside_math_block = False
        math_block_start = None
        math_blocks = []

        for line_number, line in enumerate(lines):
            if line.strip() == '```math' and not inside_math_block:
                math_block_start = line_number
                inside_math_block = True
            if line.strip() == '```' and inside_math_block:
                math_blocks.append((math_block_start, line_number))
                inside_math_block = False

        for math_block_start, math_block_end in reversed(math_blocks):
            math_lines = lines[math_block_start + 1:math_block_end]
            math_content = '\n'.join(math_lines)
            html = '<p>\n%s\n</p>\n'  # Use <p> as a wrapper
            html %= math_content
            placeholder = self.md.htmlStash.store(html)
            lines[math_block_start:math_block_end + 1] = [placeholder]
        return lines


class MathExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'enable_dollar_delimiter':
                [True, 'Enable single-dollar delimiter'],
            'add_preview': [False, 'Add a preview node before each math node'],
            'use_asciimath':
                [False, 'Use AsciiMath syntax instead of TeX syntax'],
            'use_gitlab_delimiters':
                [False, 'Use GitLab-style $`...`$ delimiters'],
        }
        super(MathExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        add_preview = self.getConfig('add_preview')
        use_asciimath = self.getConfig('use_asciimath')
        use_gitlab_delimiters = self.getConfig('use_gitlab_delimiters')
        content_type = 'math/asciimath' if use_asciimath else 'math/tex'

        inlinemathpatterns = (
            InlineMathPattern(r'(?<!\\|\$)(\$)([^\$]+)(\$)'),  # $...$
            InlineMathPattern(r'(?<!\\)(\\$)(.+?)(\\$)')  # $...$
        )
        mathpatterns = (
            DisplayMathPattern(r'(?<!\\)(\$\$)([^\$]+)(\$\$)'),  # $$...$$
            DisplayMathPattern(r'(?<!\\)(\\$$)(.+?)(\\$$)'),  # $$...$$
            DisplayMathPattern(  # \begin...\end
                r'(?<!\\)(\\begin{([a-z]+?\*?)})(.+?)(\\end{\2})')
        )
        if not self.getConfig('enable_dollar_delimiter'):
            inlinemathpatterns = inlinemathpatterns[1:]
        if use_asciimath:
            mathpatterns = mathpatterns[:-1]  # \begin...\end is TeX only
        if use_gitlab_delimiters:
            # https://gitlab.com/gitlab-org/gitlab/blob/master/doc/user/markdown.md#math
            inlinemathpatterns = (
                InlineMathPattern(r'(?<!\\)(\$`)([^`]+)(`\$)'),  # $`...`$
            )
            mathpatterns = ()
            preprocessor = GitLabPreprocessor(md)
            preprocessor._content_type = content_type
            # we should have higher priority than 'fenced_code_block' which
            # has 25
            md.preprocessors.register(preprocessor, 'math-gitlab', 27)

        for i, pattern in enumerate(mathpatterns):
            pattern._add_preview = add_preview
            pattern._content_type = content_type
            # we should have higher priority than 'escape' which has 180
            # also begin/end pattern should have lower priority than all others
            priority = 184 if i == 2 else 185
            md.inlinePatterns.register(pattern, 'math-%d' % i, priority)
        for i, pattern in enumerate(inlinemathpatterns):
            pattern._add_preview = add_preview
            pattern._content_type = content_type
            # to use gitlab delimiters, we should have higher priority than
            # 'backtick' which has 190
            priority = 195 if use_gitlab_delimiters else 185
            md.inlinePatterns.register(pattern, 'math-inline-%d' % i, priority)
        if self.getConfig('enable_dollar_delimiter'):
            md.ESCAPED_CHARS.append('$')


def makeExtension(*args, **kwargs):
    return MathExtension(*args, **kwargs)


def make_post(filepath, metadata):
    """
    make a WordPressPost for Client call
    :param filepath: 要发布的文件路径
    :param metadata: 字典类型
             包括 metadata['category']: 文章分类
                  metadata['tag']: 文章标签
                  metadata['status']: 有publish发布、draft草稿、private隐私状态可选
    :return WordPressPost: if success
            None: if failure
    """
    filename = os.path.basename(filepath)  # 例如：test(2021.11.19).md
    filename_suffix = filename.split('.')[-1]  # 例如：md
    filename_prefix = filename.split('.md')[0]  # 例如：test(2021.11.19)

    # 目前只支持 .md 后缀的文件
    if filename_suffix != 'md':
        return None

    # 1 通过frontmatter.load函数加载读取文档里的信息，包括元数据
    post_from_file = frontmatter.load(filepath)

    # 2 markdown库导入内容
    post_content_html = markdown.markdown(
        post_from_file.content,
        extensions=['markdown.extensions.fenced_code', MathExtension()],
    )
    post_content_html = post_content_html.encode("utf-8")
    # from markdown_it import MarkdownIt
    # md = MarkdownIt("gfm-like")
    # post_content_html = md.render(post_from_file.content)

    # 3 将本地post的元数据暂存到metadata中
    metadata['title'] = filename_prefix  # 将文件名去掉.md后缀，作为标题
    # metadata['slug'] = metadata['title']  # 别名
    metadata_keys = metadata.keys()
    # 如果post_from_file.metadata中的属性key存在，那么就将metadata[key]替换为它
    for key in metadata_keys:
        if (
                key in post_from_file.metadata
        ):  # 若md文件中没有元数据'category'，则无法调用post.metadata['category']
            metadata[key] = post_from_file.metadata[key]

    # 4 将metadata中的属性赋值给post的对应属性
    post = WordPressPost()  # 要返回的post
    post.content = post_content_html
    post.title = metadata['title']
    # post.slug = metadata['slug']
    post.post_status = metadata['status']
    post.terms_names = {'category': metadata['category'], 'post_tag': metadata['tag']}
    post.comment_status = 'open'  # 开启评论
    return post


def push_post(post, client):
    """
    上传post到WordPress网站
    :param post: 要发布的文章（WordPressPost类型），由make_post函数得到
    :param client: 客户端
    :return True: if success
    """
    return client.call(NewPost(post))


def get_filepaths(path):
    """
    如果path是目录路径，递归遍历path目录下的所有文件，将所有文件路径存入filepaths
    如果path是文件路径，直接将单个文件路径存入filepaths
    :param path: 你要上传的目录路径或文件路径（绝对路径）
    :return filepaths: 该目录下的所有子文件或单个文件的绝对路径
            None: wrong path
    """
    filepaths = []
    if os.path.isdir(path):  # 当前路径是目录
        for now_dirpath, child_dirnames, child_filenames in os.walk(path):
            for filename in child_filenames:
                filepath = os.path.join(now_dirpath, filename)
                filepaths.append(filepath)
        return filepaths
    elif os.path.isfile(path):  # 当前路径是文件
        return [path]
    else:  # wrong path
        return None
