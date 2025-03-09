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
