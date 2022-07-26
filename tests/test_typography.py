import unittest
from src.fluent_linter import linter
from fluent.syntax import parse


class TestTypography(unittest.TestCase):
    def checkContent(self, config, content):
        l = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))

        return l.results

    def testTE01(self):
        content = """
foo = bar's bar
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("TE01" in results[0])
        self.assertTrue("foo" in results[0])

        # Check exclusions
        config = {"TE01": {"exclusions": {"messages": ["foo"]}}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

        content = """
foo = bar ' bar
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 0)

    def testTE02(self):
        content = """
foo = bar‘s bar
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("TE02" in results[0])
        self.assertTrue("foo" in results[0])

        # Check exclusions
        config = {"TE02": {"exclusions": {"messages": ["foo"]}}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

        content = """
foo = bar ‘ bar
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 0)

    def testTE03(self):
        content = """
foo = bar 'bar' bar
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 2)
        self.assertTrue("TE01" in results[0])
        self.assertTrue("TE03" in results[1])
        self.assertTrue("foo" in results[0])

        # Check exclusions
        config = {
            "TE01": {"exclusions": {"messages": ["foo"]}},
            "TE03": {"exclusions": {"messages": ["foo"]}},
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

    def testTE04(self):
        content = """
foo = bar "bar" bar
# This shouldn't trigger an error
foo1 = { -someterm(capitalization: "uppercase") }
foo-datetime = Test: { DATETIME($timeChanged, day: "numeric", month: "long", year: "numeric") }
foo-number = { NUMBER($mem, maxFractionalUnits: 2) } MB
foo-empty = { "" }
foo-space = { "" } test
foo-curly1 = { "{" } test
foo-curly2 = { "}" } test
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("TE04" in results[0])
        self.assertTrue("foo" in results[0])

        # Check exclusions
        config = {"TE04": {"exclusions": {"messages": ["foo"]}}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

    def testTE05(self):
        content = """
foo = bar...
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("TE05" in results[0])

        # Check exclusions
        config = {"TE05": {"exclusions": {"messages": ["foo"]}}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

        content = """
foo = bar…
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 0)
