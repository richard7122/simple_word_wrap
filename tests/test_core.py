import unittest

from simple_word_wrap import wrap, wrap_lines


class WrapLinesTests(unittest.TestCase):
    def test_simple_wrap(self):
        self.assertEqual(
            wrap_lines("the quick brown fox jumps", 10),
            ["the quick", "brown fox", "jumps"],
        )

    def test_preserves_paragraph_breaks(self):
        self.assertEqual(
            wrap_lines("one two\nthree four", 20),
            ["one two", "three four"],
        )

    def test_indentation_is_reused(self):
        self.assertEqual(
            wrap_lines("    alpha beta gamma delta", 12),
            ["    alpha", "    beta", "    gamma", "    delta"],
        )

    def test_tab_indentation_is_reused(self):
        self.assertEqual(
            wrap_lines("\tone two three", 8),
            ["\tone two", "\tthree"],
        )

    def test_long_word_is_not_split(self):
        self.assertEqual(
            wrap_lines("a supercalifragilistic b", 10),
            ["a", "supercalifragilistic", "b"],
        )

    def test_blank_and_whitespace_only_lines_are_kept(self):
        self.assertEqual(wrap_lines("a\n\n   \nb", 10), ["a", "", "   ", "b"])

    def test_width_within_indent_leaves_line_alone(self):
        self.assertEqual(wrap_lines("    hello world", 4), ["    hello world"])

    def test_non_positive_width_returns_split_lines(self):
        self.assertEqual(wrap_lines("a b\nc", 0), ["a b", "c"])
        self.assertEqual(wrap_lines("a b\nc", -3), ["a b", "c"])

    def test_width_must_be_int(self):
        with self.assertRaises(TypeError):
            wrap_lines("a b", 3.0)


class WrapTests(unittest.TestCase):
    def test_wrap_joins_with_newlines(self):
        self.assertEqual(wrap("the quick brown fox", 9), "the quick\nbrown fox")

    def test_wrap_round_trips_through_wrap_lines(self):
        text = "  alpha beta gamma delta epsilon"
        self.assertEqual(wrap(text, 14), "\n".join(wrap_lines(text, 14)))

    def test_wrap_empty_string(self):
        self.assertEqual(wrap("", 10), "")


if __name__ == "__main__":
    unittest.main()
