import itertools
import re
from collections import namedtuple


Modifier = namedtuple("Modifier", "klass description")
Block = namedtuple("Block", "name description modifiers example section")

modifier_re = re.compile(r'^((?:\.|:)\S+)\s+-\s(.+)$')

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

    # group lines without an empty line in between into lists
    groups = itertools.groupby(lines, key=lambda x: x == '')
    groups = [list(b) for (blankline, b) in groups if not blankline]
    groups.reverse()

    name = groups.pop()
    if len(name) > 1:
        raise ParseError("Name can only be one line")
    name = name[0]

    while True:
        next_group = groups.pop()
        lookup = next_group[0][0]

        if lookup == '<':
            example = next_group
        elif lookup in ('.', ':'):
            modifiers = [_parse_modifier(l) for l in next_group]
        elif not groups:
            section = next_group[0].split(' ')[1]
            break
        else:
            description = next_group

    return Block(name, '\n'.join(description), modifiers, '\n'.join(example), section)


def parse(f):
    return [_parse_block(b) for b in _extract_blocks(f)]
