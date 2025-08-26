import unittest

from fluent.syntax import parse

from src.fluent_linter import linter


class TestJunk(unittest.TestCase):
    def checkContent(self, path, root, config, content):
        ftl_linter = linter.Linter(
            path, root, config, content, linter.get_offsets_and_lines(content)
        )
        ftl_linter.visit(parse(content))

        return ftl_linter.results

    def testJunk01(self):
        content = """
foo : bar
"""
        results = self.checkContent("path", "root", {}, content)
        self.assertTrue("JUNK" in results[0])
        self.assertEqual(len(results), 1)

    def testJunk02(self):
        content = """
test = { $count: ->
  [one] Test { $count}
  *[other] Test { $count}
}
"""
        results = self.checkContent("path", "root", {}, content)
        self.assertTrue("JUNK" in results[0])
        self.assertEqual(len(results), 1)
