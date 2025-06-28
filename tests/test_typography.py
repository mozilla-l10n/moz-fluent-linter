import unittest

from fluent.syntax import parse

from src.fluent_linter import linter


class TestTypography(unittest.TestCase):
    def checkContent(self, config, content):
        ftl_linter = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        ftl_linter.visit(parse(content))

        return ftl_linter.results

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

    def testTE01Disabled(self):
        """Test that TE01 can be disabled with enabled: false"""
        content = """
foo = bar's bar
"""
        # Rule enabled by default - should trigger error
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("TE01" in results[0])

        # Rule explicitly disabled - should not trigger error
        config = {"TE01": {"enabled": False}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

        # Rule explicitly enabled - should trigger error
        config = {"TE01": {"enabled": True}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("TE01" in results[0])

    def testTE02Disabled(self):
        """Test that TE02 can be disabled with enabled: false"""
        content = """
foo = bar‘s bar
"""
        # Rule enabled by default - should trigger error
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("TE02" in results[0])

        # Rule explicitly disabled - should not trigger error
        config = {"TE02": {"enabled": False}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

        # Rule explicitly enabled - should trigger error
        config = {"TE02": {"enabled": True}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("TE02" in results[0])

    def testTE03Disabled(self):
        """Test that TE03 can be disabled with enabled: false"""
        content = """
foo = bar 'test' bar
"""
        # Rule enabled by default - should trigger errors (TE01 and TE03)
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 2)
        self.assertTrue("TE01" in results[0])
        self.assertTrue("TE03" in results[1])

        # TE03 explicitly disabled - should only get TE01 error
        config = {"TE03": {"enabled": False}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("TE01" in results[0])

        # TE03 explicitly enabled - should get both errors
        config = {"TE03": {"enabled": True}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 2)
        self.assertTrue("TE01" in results[0])
        self.assertTrue("TE03" in results[1])

    def testTE04Disabled(self):
        """Test that TE04 can be disabled with enabled: false"""
        content = """
foo = bar "test" bar
"""
        # Rule enabled by default - should trigger error
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("TE04" in results[0])

        # Rule explicitly disabled - should not trigger error
        config = {"TE04": {"enabled": False}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

        # Rule explicitly enabled - should trigger error
        config = {"TE04": {"enabled": True}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("TE04" in results[0])

    def testTE05Disabled(self):
        """Test that TE05 can be disabled with enabled: false"""
        content = """
foo = bar...
"""
        # Rule enabled by default - should trigger error
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("TE05" in results[0])

        # Rule explicitly disabled - should not trigger error
        config = {"TE05": {"enabled": False}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

        # Rule explicitly enabled - should trigger error
        config = {"TE05": {"enabled": True}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("TE05" in results[0])
