from jinja2 import Environment, PackageLoader
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import HtmlLexer

from .parser import parse


env = Environment(loader=PackageLoader('gerrard', '.'))


def highlight_html(value):
    return highlight(value, HtmlLexer(), HtmlFormatter())

env.filters['highlight_html'] = highlight_html


class Styleguide(object):

    def __init__(self):
        self.blocks = []

    def add_file(self, f):
        self.blocks.extend(parse(f))

    def sort(self):
        """Sort the blocks according to their section number."""
        def key(obj):
            return map(int, obj.section.rstrip('.').split('.'))

        self.blocks.sort(key=key)


def generate(css_file, blocks):
    """Generate complete styleguide.

    css_file - Path to the CSS file that contains the actual styles
    blocks   - List of blocks that should be included in the guide

    Returns the styleguide as HTML.
    """
    template = env.get_template('template.html')
    context = {
        'css_file': css_file,
        'blocks': blocks,
        'pygments_highlight': HtmlFormatter().get_style_defs('.highlight')

    }
    return template.render(**context)
