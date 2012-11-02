import functools
import re
from collections import namedtuple
from itertools import takewhile


Modifier = namedtuple("Modifier", "klass description")
Block = namedtuple("Block", "name description modifiers example section")

modifier_re = re.compile(r'^(\.\S+)\s+-\s(.+)$')

class ParseError(Exception): pass


def _extract_blocks(f):
    current_block = []

    for line in f:
        if not line.startswith('//'):
            if current_block and 'Styleguide' in current_block[-1]:
                yield current_block
            
            current_block = []
            continue

        current_block.append(line[3:].rstrip())


def _parse_modifier(line):
    try:
        klass, description = modifier_re.findall(line)[0]
    except IndexError:
        raise ParseError("'%s' is not a valid modifier line" % line)
    return Modifier(klass.strip(), description.strip())


def _parse_block(lines):
    name = None
    description = []
    modifiers = []
    example = []
    section = ""

    until_blank = functools.partial(takewhile, lambda x: x!= '')

    it = iter(lines)
    try:
        name = next(it)
        next(it)

        description = list(until_blank(it))

        line = next(it)
        if line.startswith('.'):
            # modifiers
            modifiers.append(_parse_modifier(line))
            modifiers.extend(_parse_modifier(l) for l in until_blank(it))
        else:
            # no modifiers, line belongs to example
            example.append(line)

        example.extend(until_blank(it))

        section = next(it)
        section = section.split(' ')[1]
    except StopIteration:
        raise ParseError()

    return Block(name, '\n'.join(description), modifiers, '\n'.join(example), section)


def parse(f):
    return [_parse_block(b) for b in _extract_blocks(f)]
