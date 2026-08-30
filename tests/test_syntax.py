import unittest

from fluent.syntax import parse

from src.fluent_linter import linter


class TestSyntax(unittest.TestCase):
    def checkContent(self, config, content):
        ftl_linter = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        ftl_linter.visit(parse(content))

        return ftl_linter.results

    def testSY01(self):
        content = """
-foo = bar
"""
        config = {"SY01": {"disabled": True}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("SY01" in results[0])
        # The message ID should be the term name, not a serialized AST node.
        self.assertTrue("Message ID: foo" in results[0])
        self.assertTrue("Identifier" not in results[0])

    def testSY02(self):
        content = """
foo = { foo1 }
"""
        config = {"SY02": {"disabled": True}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("SY02" in results[0])

    def testSY03(self):
        content = """
foo = { -foo1 }
"""
        config = {"SY03": {"disabled": True}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("SY03" in results[0])

    def testSY04(self):
        content = """
foo = { $x ->
    [a] bar1
   *[b] bar2
}
"""
        config = {"SY04": {"disabled": True}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("SY04" in results[0])

    def testSY05(self):
        content = """
foo = bar
    .test = bar 1
"""
        config = {"SY05": {"disabled": True}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("SY05" in results[0])

    def testSY06(self):
        content = """
foo = { $foovar }
"""
        config = {"SY06": {"disabled": True}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("SY06" in results[0])

    def testSY07(self):
        # Localized plural categories never match: this is the bug the rule
        # exists to catch.
        content = """
foo = { $count ->
    [uno] bar1
   *[otro] bar2
}
"""
        config = {"SY07": {"enabled": True}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 2)
        self.assertTrue("SY07" in results[0])
        self.assertTrue("uno" in results[0])
        self.assertTrue("otro" in results[1])
        self.assertTrue("Message ID: foo" in results[0])

    def testSY07_valid(self):
        # Plural categories and number literals are both accepted.
        content = """
foo = { $count ->
    [0] bar0
    [one] bar1
    [few] bar2
   *[other] bar3
}
"""
        config = {"SY07": {"enabled": True}}
        self.assertEqual(len(self.checkContent(config, content)), 0)

    def testSY07_disabled_by_default(self):
        content = """
foo = { $count ->
    [uno] bar1
   *[otro] bar2
}
"""
        self.assertEqual(len(self.checkContent({}, content)), 0)
        self.assertEqual(
            len(self.checkContent({"SY07": {"enabled": False}}, content)), 0
        )

    def testSY07_function_selector(self):
        # PLATFORM() and other function selects are free form by design.
        content = """
foo = { PLATFORM() ->
    [windows] bar1
    [macos] bar2
   *[other] bar3
}
"""
        config = {"SY07": {"enabled": True}}
        self.assertEqual(len(self.checkContent(config, content)), 0)

    def testSY07_exclusions(self):
        content = """
foo = { $count ->
    [uno] bar1
   *[otro] bar2
}
"""
        config = {
            "SY07": {"enabled": True, "exclusions": {"messages": ["foo"], "files": []}}
        }
        self.assertEqual(len(self.checkContent(config, content)), 0)
