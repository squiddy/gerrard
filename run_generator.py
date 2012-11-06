import sys

from gerrard import generate, Styleguide


if __name__ == '__main__':
    css_file = sys.argv[1]
    guide = Styleguide()

    for filename in sys.argv[2:]:
        with open(filename) as f:
            guide.add_file(f)

    guide.sort()

    print generate(css_file, guide.blocks)
