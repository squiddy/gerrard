import StringIO
import unittest

from gerrard import ParseError
from gerrard.parser import _extract_blocks, Modifier, Block


class ModifierParserTest(unittest.TestCase):
    """Test the supported modifier types and different notations."""

    def test_parse_modifier(self):
        mod = Modifier.parse(".foobar - Test")
        self.assertEqual(mod.klass, ".foobar")
        self.assertEqual(mod.description, "Test")

        mod = Modifier.parse(".foobar-baz - Test-2")
        self.assertEqual(mod.klass, ".foobar-baz")
        self.assertEqual(mod.description, "Test-2")

        mod = Modifier.parse(".foobar-baz   -   Test-3")
        self.assertEqual(mod.klass, ".foobar-baz")
        self.assertEqual(mod.description, "Test-3")

    def test_parse_pseudo_class_modifier(self):
        mod = Modifier.parse(":hover - Test-4")
        self.assertEqual(mod.klass, ":hover")
        self.assertEqual(mod.description, "Test-4")

    def test_incomplete_modifier_raises_error(self):
        self.assertRaises(ParseError, Modifier.parse, ".foobar")
        self.assertRaises(ParseError, Modifier.parse, ".foobar - ")


class BlockParserTest(unittest.TestCase):
    """Test that the block parsing handles optional fields."""

    def test_parse_complete_block(self):
        value = """
Name

Description Line 1
Description Line 2

.modifier1 - Modifier1
.modifier2 - Modifier2

<div>
  Foobar
</div>

Styleguide 1.2
        """.strip().splitlines()

        block = Block.parse(value)

        self.assertEqual(block.name, "Name")
        self.assertEqual(block.description, "Description Line 1\nDescription Line 2")
        self.assertEqual(len(block.modifiers), 2)
        self.assertEqual(block.modifiers[0].klass, ".modifier1")
        self.assertEqual(block.modifiers[0].description, "Modifier1")
        self.assertEqual(block.modifiers[1].klass, ".modifier2")
        self.assertEqual(block.modifiers[1].description, "Modifier2")
        self.assertEqual(block.example, "<div>\n  Foobar\n</div>")
        self.assertEqual(block.section, "1.2")
        self.assertFalse(block.is_module)

    def test_parse_block_without_modifiers(self):
        value = """
Name

Description Line 1
Description Line 2

<div>
  Foobar
</div>

Styleguide 1.2
        """.strip().splitlines()

        block = Block.parse(value)

        self.assertEqual(block.name, "Name")
        self.assertEqual(block.description, "Description Line 1\nDescription Line 2")
        self.assertEqual(len(block.modifiers), 0)
        self.assertEqual(block.example, "<div>\n  Foobar\n</div>")
        self.assertEqual(block.section, "1.2")
        self.assertFalse(block.is_module)

    def test_parse_block_without_description(self):
        value = """
Name

.modifier1 - Modifier1

<div>
  Foobar
</div>

Styleguide 1.2
        """.strip().splitlines()

        block = Block.parse(value)

        self.assertEqual(block.name, "Name")
        self.assertEqual(block.description, "")
        self.assertEqual(len(block.modifiers), 1)
        self.assertEqual(block.modifiers[0].klass, ".modifier1")
        self.assertEqual(block.modifiers[0].description, "Modifier1")
        self.assertEqual(block.example, "<div>\n  Foobar\n</div>")
        self.assertEqual(block.section, "1.2")
        self.assertFalse(block.is_module)

    def test_parse_minimal_block(self):
        value = """
Name

Styleguide 1.2
        """.strip().splitlines()

        block = Block.parse(value)

        self.assertEqual(block.name, "Name")
        self.assertEqual(block.description, "")
        self.assertEqual(len(block.modifiers), 0)
        self.assertEqual(block.example, "")
        self.assertEqual(block.section, "1.2")
        self.assertTrue(block.is_module)


class ParserTest(unittest.TestCase):

    def test_extract_blocks(self):
        """Test that blocks are detected correctly and slashes are removed."""
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
        self.assertEqual(blocks[0], ["Block1", "", "foobar", "", "Styleguide"])
        self.assertEqual(blocks[1], ["Block2", "", "Styleguide"])


if __name__ == '__main__':
    unittest.main()
