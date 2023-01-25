import unittest
from src.fluent_linter import linter
from fluent.syntax import parse


class TestCommentVariables(unittest.TestCase):
    def checkContent(self, config, content):
        l = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))

        return l.results

    def testVC01(self):
        content = """
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

### $var doesn't count towards commented placeables

message-without-comment = This string has a { $var }
"""
        config = {
            "VC": {
                "disabled": False,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("VC01" in results[0])

        results = self.checkContent({}, content)
        self.assertEqual(len(results), 0)

    def testVC02(self):
        content = """


## Variables:
## $foo-group (String): group level comment

# Variables:
# $foo1 (String): just text
message-with-comment = This string has a { $foo1 }

message-with-group-comment = This string has a { $foo-group }
"""
        config = {
            "VC": {
                "disabled": False,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

    def testVC03(self):
        content = """
select-without-comment1 = {
    $select1 ->
        [t] Foo
       *[s] Bar
}

select-without-comment2 = {
    $select2 ->
        [t] Foo { $select2 }
       *[s] Bar
}
"""
        config = {
            "VC": {
                "disabled": False,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 2)
        self.assertTrue("VC01" in results[0])
        self.assertTrue("$select1" in results[0])
        self.assertTrue("$select2" in results[1])

        results = self.checkContent({}, content)
        self.assertEqual(len(results), 0)

    def testVC04(self):
        content = """
message-attribute-without-comment =
    .label = This string as { $attr }

# Variables:
# $attr (String): just text
message-attribute-with-comment =
    .label = This string as { $attr }
"""
        config = {
            "VC": {
                "disabled": False,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 1)
        self.assertTrue("VC01" in results[0])
        self.assertTrue("$attr" in results[0])

        results = self.checkContent({}, content)
        self.assertEqual(len(results), 0)

    def testVC05(self):
        content = """
message-selection-function =
  { PLATFORM() ->
      [macos] foo
     *[other] bar
  }
"""
        config = {
            "VC": {
                "disabled": False,
            }
        }
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)
