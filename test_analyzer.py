import unittest
from opendevkit.analyzer import analyze_source

class AnalyzerTests(unittest.TestCase):
    def test_valid_source(self):
        result = analyze_source('def hello():\n    """Greet."""\n    return 1\n')
        self.assertTrue(result['valid'])
        self.assertEqual(result['functions'], ['hello'])
        self.assertEqual(result['findings'], [])

    def test_syntax_error(self):
        self.assertFalse(analyze_source('def broken(:')['valid'])

    def test_bare_except(self):
        result = analyze_source('try:\n    pass\nexcept:\n    pass\n')
        self.assertIn('BARE_EXCEPT', [x['code'] for x in result['findings']])

    def test_dynamic_execution(self):
        result = analyze_source('eval("1+1")')
        self.assertIn('DYNAMIC_EXEC', [x['code'] for x in result['findings']])

if __name__ == '__main__':
    unittest.main()
