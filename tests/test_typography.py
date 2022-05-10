import unittest
from src.fluent_linter import linter
from fluent.syntax import parse


class TestTypography(unittest.TestCase):
    def testTE01(self):
        content = """
foo = bar's bar
"""
        l = linter.Linter(
            "path", "root", {}, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 1)
        self.assertTrue("TE01" in results[0])

        # Check exclusions
        config = {"TE01": {"exclusions": {"messages": ["foo"]}}}
        l = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 0)

        content = """
foo = bar ' bar
"""
        l = linter.Linter(
            "path", "root", {}, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 0)

    def testTE02(self):
        content = """
foo = bar‘s bar
"""
        l = linter.Linter(
            "path", "root", {}, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 1)
        self.assertTrue("TE02" in results[0])

        # Check exclusions
        config = {"TE02": {"exclusions": {"messages": ["foo"]}}}
        l = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 0)

        content = """
foo = bar ‘ bar
"""
        l = linter.Linter(
            "path", "root", {}, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 0)

    def testTE03(self):
        content = """
foo = bar 'bar' bar
"""
        l = linter.Linter(
            "path", "root", {}, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 2)
        self.assertTrue("TE01" in results[0])
        self.assertTrue("TE03" in results[1])

        # Check exclusions
        config = {
            "TE01": {"exclusions": {"messages": ["foo"]}},
            "TE03": {"exclusions": {"messages": ["foo"]}},
        }
        l = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 0)

    def testTE04(self):
        content = """
foo = bar "bar" bar
# This shouldn't trigger an error
foo1 = { -someterm(capitalization: "uppercase") }
"""
        l = linter.Linter(
            "path", "root", {}, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 1)
        self.assertTrue("TE04" in results[0])

        # Check exclusions
        config = {"TE04": {"exclusions": {"messages": ["foo"]}}}
        l = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 0)

    def testTE05(self):
        content = """
foo = bar...
"""
        l = linter.Linter(
            "path", "root", {}, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 1)
        self.assertTrue("TE05" in results[0])

        # Check exclusions
        config = {"TE05": {"exclusions": {"messages": ["foo"]}}}
        l = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 0)

        content = """
foo = bar…
"""
        l = linter.Linter(
            "path", "root", {}, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 0)
