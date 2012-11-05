from jinja2 import Environment, PackageLoader
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import HtmlLexer


env = Environment(loader=PackageLoader('gerrard', '.'))


def highlight_html(value):
    return highlight(value, HtmlLexer(), HtmlFormatter())

env.filters['highlight_html'] = highlight_html


def generate(css_file, blocks):
    template = env.get_template('template.html')
    context = {
        'css_file': css_file,
        'blocks': blocks,
        'pygments_highlight': HtmlFormatter().get_style_defs('.highlight')

    }
    return template.render(**context)
