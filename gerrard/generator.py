from jinja2 import Environment
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import HtmlLexer


env = Environment()


style = """
body {
  background: none;
  color: black;
  padding: 20px;
  padding-left: 200px;
  width: 600px;
}

h2 {
  color: #fff;
  padding: 3px;
  border-bottom: 5px solid #A7DBD8;
  background: #69D2E7;
}

.block {
  padding: 0px 10px;
}

.block-example {
  position: relative;
  padding: 10px;
  padding-top: 20px;
  border: 2px solid #eee;
  margin-bottom: 5px;
}

.block-example-modifier {
  position: absolute;
  right: 0;
  top: 0;
  background: #aaa;
  color: white;
  padding: 2px 3px;
  font-style: normal;
  font-size: 11px;
}

.block-modifiers {
  width: 100%;
  margin-bottom: 10px;
}

.block-modifiers td:first-child {
  width: 30%;
}

code pre {
  background: #E0E4CC;
  padding: 10px;
}

"""

html = """
<!DOCTYPE html>
<html>
  <head>
    <title>gerrard</title>
    <link rel="stylesheet" href="{{ css_file }}" />
    <style>
      {{ base_style }}
    </style>
    <style>
      {{ pygments_highlight }}
    </style>
  </head>
  <body>
    <h1>Styleguide</h1>

    {% for block in blocks %}
      <h2>{{ block.section }} {{ block.name }}</h2>
      <div class="block">

      {% if block.description %}
        <p>{{ block.description }}</p>
      {% endif %}

      {% if block.modifiers %}
        <table class="block-modifiers">
          {% for mod in block.modifiers %}
          <tr>
            <td>{{ mod.klass }}</td><td>{{ mod.description }}</td>
          </tr>
          {% endfor %}
        </table>
      {% endif %}

      {% if block.example %}
        <div class="block-example">
          {{ block.example.replace('$modifier', '') }}
        </div>
        {% for mod in block.modifiers %}
          <div class="block-example">
            <em class="block-example-modifier">{{ mod.klass }}</em>
            {{ block.example.replace('$modifier', mod.markup_class) }}
          </div>
        {% endfor %}
        <code>{{ block.example|highlight_html }}</code>
      {% endif %}
      </div>
    {% endfor %}

  </body>
</html>
"""

def highlight_html(value):
    return highlight(value, HtmlLexer(), HtmlFormatter())

env.filters['highlight_html'] = highlight_html


def generate(css_file, blocks):
    template = env.from_string(html)
    context = {
        'css_file': css_file,
        'blocks': blocks,
        'base_style': style,
        'pygments_highlight': HtmlFormatter().get_style_defs('.highlight')

    }
    return template.render(**context)
