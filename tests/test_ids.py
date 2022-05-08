import unittest
from src.fluent_linter import linter
from fluent.syntax import parse


class TestIDs(unittest.TestCase):
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

        l = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 5)

        # Test file exclusion
        l = linter.Linter(
            "path/foo", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
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

        l = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 2)

        # Test file exclusion
        l = linter.Linter(
            "path/foo", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))
        results = l.results
        self.assertEqual(len(results), 0)
