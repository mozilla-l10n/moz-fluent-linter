import unittest
from src.fluent_linter import linter
from fluent.syntax import parse


class TestVariableStyle(unittest.TestCase):
    def checkContent(self, config, content):
        l = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))

        return l.results

    def testVS01_valid(self):
        content = """
foo = { $foovar }
"""
        config = {"VS01": {"disabled": False}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

    def testVS01_invalid_preceding(self):
        content = """
foo = {$foovar }
"""
        config = {"VS01": {"disabled": False}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("VS01" in results[0])

    def testVS01_invalid_following(self):
        content = """
foo = { $foovar}
"""
        config = {"VS01": {"disabled": False}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("VS01" in results[0])
