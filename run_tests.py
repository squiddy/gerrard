import StringIO
import unittest

from gerrard import parse, ParseError
from gerrard.parser import _extract_blocks, _parse_modifier


class ParserTest(unittest.TestCase):

    def test_extract_blocks(self):
        f = StringIO.StringIO("""
// No block
.foobar {}

// Block1
//
// foobar
//
// Styleguide
div {}

// Block2
// 
// Styleguide
        """)

        blocks = list(_extract_blocks(f))
        self.assertEqual(len(blocks), 2)

    def test_parse_modifier(self):
        mod = _parse_modifier(".foobar - Test")
        self.assertEqual(mod.klass, ".foobar")
        self.assertEqual(mod.description, "Test")

        mod = _parse_modifier(".foobar-baz - Test-2")
        self.assertEqual(mod.klass, ".foobar-baz")
        self.assertEqual(mod.description, "Test-2")

        mod = _parse_modifier(".foobar-baz   -   Test-3")
        self.assertEqual(mod.klass, ".foobar-baz")
        self.assertEqual(mod.description, "Test-3")

        mod = _parse_modifier(":hover - Test-4")
        self.assertEqual(mod.klass, ":hover")
        self.assertEqual(mod.description, "Test-4")

        self.assertRaises(ParseError, _parse_modifier, ".foobar")
        self.assertRaises(ParseError, _parse_modifier, ".foobar - ")

    def test_parse_complete_block(self):
        f = StringIO.StringIO("""
// Name
//
// Description Line 1
// Description Line 2
//
// .modifier1 - Modifier1
// .modifier2 - Modifier2
//
// <div>
//   Foobar
// </div>
//
// Styleguide 1.2
.foobar {

}
        """)

        blocks = parse(f)
        self.assertEqual(len(blocks), 1)
        block = blocks[0]

        self.assertEqual(block.name, "Name")
        self.assertEqual(block.description, "Description Line 1\nDescription Line 2")
        self.assertEqual(len(block.modifiers), 2)
        self.assertEqual(block.modifiers[0].klass, ".modifier1")
        self.assertEqual(block.modifiers[0].description, "Modifier1")
        self.assertEqual(block.modifiers[1].klass, ".modifier2")
        self.assertEqual(block.modifiers[1].description, "Modifier2")
        self.assertEqual(block.example, "<div>\n  Foobar\n</div>")
        self.assertEqual(block.section, "1.2")

    def test_parse_block_without_modifiers(self):
        f = StringIO.StringIO("""
// Name
//
// Description Line 1
// Description Line 2
//
// <div>
//   Foobar
// </div>
//
// Styleguide 1.2
.foobar {

}
        """)

        blocks = parse(f)
        self.assertEqual(len(blocks), 1)
        block = blocks[0]

        self.assertEqual(block.name, "Name")
        self.assertEqual(block.description, "Description Line 1\nDescription Line 2")
        self.assertEqual(len(block.modifiers), 0)
        self.assertEqual(block.example, "<div>\n  Foobar\n</div>")
        self.assertEqual(block.section, "1.2")


if __name__ == '__main__':
    unittest.main()
