from jinja2 import Template

html = """
<!DOCTYPE html>
<html>
  <head>
    <title>gerrard</title>
    <link rel="stylesheet" href="{{ css_file }}" />
  </head>
  <body>
    <h1>Styleguide</h1>

    {% for block in blocks %}
      <h2>{{ block.section }} {{ block.name }}</h2>

      {% if block.description %}
        <p>{{ block.description }}</p>
      {% endif %}

      {% if block.modifiers %}
        <table>
          {% for mod in block.modifiers %}
          <tr>
            <td>{{ mod.klass }}</td><td>{{ mod.description }}</td>
          </tr>
          {% endfor %}
        </table>
      {% endif %}

      {% if block.example %}
        <div class="modifier-example">
          {{ block.example.replace('$modifier', '') }}
        </div>
        {% for mod in block.modifiers %}
          <div class="modifier-example">
            {{ block.example.replace('$modifier', mod.markup_class) }}
          </div>
        {% endfor %}
        <code><pre>{{ block.example|escape }}</pre></code>
      {% endif %}
    {% endfor %}

  </body>
</html>
"""

def generate(css_file, blocks):
    template = Template(html)
    return template.render(css_file=css_file, blocks=blocks)
