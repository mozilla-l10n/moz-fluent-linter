import unittest
from src.fluent_linter import linter
from fluent.syntax import parse


class TestBrands(unittest.TestCase):
    def checkContent(self, config, content):
        l = linter.Linter(
            "file.ftl", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))

        return l.results

    def testCO01(self):
        content = """
bad-firefox1 = Welcome to Firefox

# Comment should be ignored when displaying the offset of the error
bad-firefox2 = Welcome to Firefox again
bad-firefox2b = <span>Welcome to Firefox<span> again
bad-firefox3 = <b>Firefox</b>
bad-firefox-excluded = <b>Firefox</b>

bad-mozilla1 = Welcome to Mozilla
bad-mozilla2 = Welcome to Mozilla again
bad-mozilla2b = <span>Welcome to Mozilla</span> again
bad-mozilla3 = <b>Mozilla</b>

good-firefox1 = Welcome to { -brand-firefox }
good-firefox2 = Welcome to { firefox-message }

good-mozilla1 = Welcome to { -brand-mozilla }
good-mozilla2 = Welcome to { mozilla-message }
"""

        config = {
            "CO01": {
                "enabled": False,
                "brands": [],
                "exclusions": {
                    "messages": [],
                    "files": [],
                },
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

        config = {
            "CO01": {
                "enabled": True,
                "brands": ["Firefox", "Mozilla"],
                "exclusions": {
                    "messages": ["bad-firefox-excluded"],
                    "files": [],
                },
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 8)
        self.assertTrue("CO01" in results[0])
        self.assertTrue("line 5" in results[1])

        config = {
            "CO01": {
                "enabled": True,
                "brands": ["Firefox", "Mozilla"],
                "exclusions": {
                    "messages": [],
                    "files": ["file.ftl"],
                },
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)
