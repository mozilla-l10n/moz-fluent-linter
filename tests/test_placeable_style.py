import unittest
from src.fluent_linter import linter
from fluent.syntax import parse


class TestPlaceableStyle(unittest.TestCase):
    def checkContent(self, config, content):
        l = linter.Linter(
            "path", "root", config, content, linter.get_offsets_and_lines(content)
        )
        l.visit(parse(content))

        return l.results

    def testPS01_valid(self):
        content = """
foo-var = { $foovar }
foo-message = { some-message }
foo-term = { -some-term }
"""
        config = {"PS01": {"disabled": False}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)

    def testPS01_invalid_preceding(self):
        content = """
foo-var= {$foovar }
foo-message = {some-message }
foo-term = {-some-term }
"""
        config = {"PS01": {"disabled": False}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 3)
        self.assertTrue("PS01" in results[0])

    def testPS01_invalid_following(self):
        content = """
foo-var= { $foovar}
foo-message = { some-message}
foo-term = { -some-term}
"""
        config = {"PS01": {"disabled": False}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 3)
        self.assertTrue("PS01" in results[0])

    def testPS01_invalid_multiple(self):
        content = """
foo-var= {  $foovar  }
foo-var1= {$foovar  }
foo-var2= {  $foovar}
foo-message = {  some-message  }
foo-message1 = {some-message  }
foo-message2 = {  some-message}
foo-term = {  -some-term  }
foo-term1 = {-some-term  }
foo-term2 = {  -some-term}
"""
        config = {"PS01": {"disabled": False}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 18)
        self.assertTrue("PS01" in results[0])

    def testPS01_select(self):
        content = """
select-expression = {
    $select-var ->
        [t] Foo { $select-var }
       *[s] Bar
}
"""
        config = {"PS01": {"disabled": False}}
        results = self.checkContent(config, content)
        self.assertEqual(len(results), 0)
