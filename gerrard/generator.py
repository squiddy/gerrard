from jinja2 import Environment, PackageLoader
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import HtmlLexer


env = Environment(loader=PackageLoader('gerrard', '.'))


def highlight_html(value):
    return highlight(value, HtmlLexer(), HtmlFormatter())

env.filters['highlight_html'] = highlight_html


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
