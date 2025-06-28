import unittest

from fluent.syntax import parse

from src.fluent_linter import linter


class TestIDs(unittest.TestCase):
    def checkContent(self, path, root, config, content):
        ftl_linter = linter.Linter(
            path, root, config, content, linter.get_offsets_and_lines(content)
        )
        ftl_linter.visit(parse(content))

        return ftl_linter.results

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

    def testID03(self):
        test_cases = [
            ("hello.world", "Identifiers cannot contain dots"),
            ("hello world", "Identifiers cannot contain spaces"),
            ("1hello", "Identifiers cannot start with a number"),
            ("9test", "Identifiers cannot start with a number"),
        ]
        for test_id, expected_msg in test_cases:
            with self.subTest(test_id=test_id):
                content = f"{test_id} = bar"
                config = {"ID03": {"enabled": True}}
                results = self.checkContent("path", "root", config, content)
                self.assertGreater(
                    len(results),
                    0,
                    f"Expected '{test_id}' to be invalid but got no errors",
                )
                self.assertIn(
                    expected_msg,
                    results[0],
                    f"Expected error message '{expected_msg}' for '{test_id}'",
                )

        # Test that valid identifiers are not flagged (including those ending with hyphens)
        valid_ids = [
            "valid-term",
            "hello-",
            "-hello",
            "test-world-",
            "ending-with-hyphen-",
        ]
        for valid_id in valid_ids:
            with self.subTest(valid_id=valid_id):
                content = f"{valid_id} = bar"
                config = {"ID03": {"enabled": True}}
                results = self.checkContent("path", "root", config, content)
                self.assertEqual(
                    len(results),
                    0,
                    f"Valid identifier '{valid_id}' should not be flagged",
                )

        # Test that valid terms (starting with -) are not flagged
        content = "-valid-term = bar"
        config = {"ID03": {"enabled": True}}
        results = self.checkContent("path", "root", config, content)
        self.assertEqual(len(results), 0, "Valid terms should not be flagged")

    def testInvalidIDs(self):
        # Test case for empty identifier
        content = "= bar"
        config = {"ID03": {"enabled": True}}
        results = self.checkContent("path", "root", config, content)
        # Note: Empty identifiers cause parse errors, so this is handled by the parser itself
        self.assertGreater(len(results), 0, "Empty identifiers should be detected")
