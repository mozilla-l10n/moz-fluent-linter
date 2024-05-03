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

bad-monitor = Monitor your email
good-monitor = Monitored emails
good-monitor2 = Set up your monitor.

bad-account = Set up your { -brand-short-name } account
good-account = Set up your { -brand-short-name }. Account.
good-account2 = Set up your { -brand-short-name } Account.
"""

        config = {
            "CO01": {
                "enabled": False,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

        config = {
            "CO01": {
                "enabled": True,
                "brands": ["Firefox", "Mozilla", "{ -brand-short-name } account"],
                "exclusions": {
                    "messages": ["bad-firefox-excluded"],
                },
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 9)
        self.assertTrue("CO01" in results[0])
        self.assertTrue("Firefox" in results[0])
        self.assertTrue("line 4" in results[1])
        self.assertTrue("bad-firefox2" in results[1])
        self.assertTrue("Mozilla" in results[5])
        self.assertTrue("{ -brand-short-name } account" in results[8])

        config = {
            "CO01": {
                "enabled": True,
                "brands": ["Firefox", "Mozilla"],
                "exclusions": {
                    "files": ["file.ftl"],
                },
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

        config = {"CO01": {"enabled": True, "brands": ["Monitor"], "exclusions": {}}}
        results = self.checkContent(config, content)
        print("\n".join(results))
        self.assertEqual(len(results), 1)
        self.assertTrue("bad-monitor" in results[0])
        self.assertTrue("good-monitor" not in results[0])
