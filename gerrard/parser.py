import itertools
import re
from collections import namedtuple


class ParseError(Exception):
    """Raised when the input doesn't match the specification."""
    pass


class Modifier(namedtuple("Modifier", "klass description")):
    """Represents a class/pseudo selector that belongs to a block."""

    MODIFIER_RE = re.compile(r'^((?:\.|:)\S+)\s+-\s(.+)$')

    @property
    def markup_class(self):
        """Class to be used when generating html."""
        if self.klass.startswith('.'):
            return self.klass[1:]

        return self.klass

    @classmethod
    def parse(cls, line):
        try:
            klass, description = cls.MODIFIER_RE.findall(line)[0]
        except IndexError:
            raise ParseError("'%s' is not a valid modifier line" % line)

        return cls(klass.strip(), description.strip())


class Block(namedtuple("Block", "name description modifiers example section")):
    """Represents a single piece of the styleguide.

    A block must have a name and a section identifier. Description, modifier
    and html example are optional.

    Example of a block in the stylesheets:

        // Button
        //
        // Description of the button style.
        //
        // .button-primary - Use to get the visitor's attention
        //
        // <a href="button $modifier">Linktext</a>
        //
        // Styleguide 1.1
    """

    @classmethod
    def parse(cls, lines):
        name = None
        description = ""
        modifiers = []
        example = ""
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
                example = '\n'.join(next_group)
            elif lookup in ('.', ':'):
                modifiers = [Modifier.parse(l) for l in next_group]
            elif not groups:
                section = next_group[0].split(' ')[1]
                break
            else:
                description = '\n'.join(next_group)

        return cls(name, description, modifiers, example, section)


def _extract_blocks(file_obj):
    """Yields groups of lines that match the block spec."""
    current_block = []

    for line in file_obj:
        if not line.startswith('//'):
            if current_block and 'Styleguide' in current_block[-1]:
                yield current_block

            current_block = []
            continue

        current_block.append(line[3:].rstrip())


def parse(file_obj):
    """Return list of blocks found in the file."""
    return [Block.parse(b) for b in _extract_blocks(file_obj)]
