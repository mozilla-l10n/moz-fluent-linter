import unittest
from src.fluent_linter import linter
from fluent.syntax import parse


class TestIDs(unittest.TestCase):
    def checkContent(self, path, root, config, content):
        l = linter.Linter(
            path, root, config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))

        return l.results

    def testID01(self):
        content = """
foo = bar
fooTest = bar
-footerm = bar
-fooTerm = bar
foo-test = bar
foo-Test = bar
foo_test = bar
foo_Test = bar
foo_Test-ex = bar
"""
        config = {
            "ID01": {
                "enabled": True,
                "exclusions": {
                    "files": ["path/foo"],
                    "messages": [
                        "foo_Test-ex",
                    ],
                },
            }
        }

        results = self.checkContent("path", "root", config, content)
        self.assertTrue("fooTest" in results[0])
        self.assertTrue("-fooTerm" in results[1])

        # Test file exclusion
        results = self.checkContent("path/foo", "root", config, content)
        self.assertEqual(len(results), 0)

    def testID02(self):
        content = """
foo = bar
foo-test1 = bar
foo-test-long-id = bar
foo1= bar
"""
        config = {
            "ID02": {
                "enabled": True,
                "min_length": 10,
                "exclusions": {
                    "files": ["path/foo"],
                    "messages": [
                        "foo1",
                    ],
                },
            }
        }

        results = self.checkContent("path", "root", config, content)
        self.assertEqual(len(results), 2)
        self.assertTrue("foo" in results[0])

        # Test file exclusion
        results = self.checkContent("path/foo", "root", config, content)
        self.assertEqual(len(results), 0)
