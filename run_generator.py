import sys

from gerrard import parse, generate


if __name__ == '__main__':
    blocks = []
    css_file = sys.argv[1]

    for filename in sys.argv[2:]:
        with open(filename) as f:
            blocks.extend(parse(f))

    print generate(css_file, blocks)
