import unittest

from fluent.syntax import parse

from src.fluent_linter import linter


class TestComments(unittest.TestCase):
    def checkContent(self, config, content):
        ftl_linter = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        ftl_linter.visit(parse(content))

        return ftl_linter.results

    def testGC01(self):
        content = """
foo = bar

## Group comment
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("GC01" in results[0])

        config = {
            "GC": {
                "disabled": True,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

    def testGC02(self):
        content = """
## Group comment
foo = bar
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("GC02" in results[0])

        config = {
            "GC": {
                "disabled": True,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

    def testGC03(self):
        content = """
## Group comment

foo = bar
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("GC03" in results[0])

        config = {
            "GC": {
                "disabled": True,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

    def testGC04(self):
        content = """
foo1 = test

## Group comment

## Another group comment

foo = bar
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("GC04" in results[0])

        config = {
            "GC": {
                "disabled": True,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

    def testRC01(self):
        content = """
foo = bar

### Resource comment

foo1 = bar
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("RC01" in results[0])

        config = {
            "RC": {
                "disabled": True,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

    def testRC02(self):
        content = """
### Resource comment
foo = bar
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("RC02" in results[0])

        config = {
            "RC": {
                "disabled": True,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

    def testRC03(self):
        content = """
### Resource comment

foo = bar
"""
        results = self.checkContent({}, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("RC03" in results[0])

        config = {
            "RC": {
                "disabled": True,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)
