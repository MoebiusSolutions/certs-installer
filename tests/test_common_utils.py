import unittest
import re
from moesol.common_utils import find_sections
from moesol.common_utils import simple_pattern_to_regex

class MoesolCommonUtils(unittest.TestCase):

	def test_find_sections(self):
		"""
		Verifies basic function of fine_sections()
		"""
		content = (
			'Ignore Leading\n'
			'== START ==\n'
			'SECTION 1, LINE 1\n'
			'SECTION 1, LINE 2\n'
			'SECTION 1, LINE 3\n'
			'== END ==\n'
			'Ignore Middle 1\n'
			'Ignore Middle 2\n'
			'== START ==\n'
			'SECTION 2, LINE 2\n'
			'== END ==\n'
			'Ignore End\n' )
		result = find_sections(content, re.compile('== START =='), re.compile('== END =='))

		self.assertEqual(len(result), 2)
		expected = (
			'== START ==\n'
			'SECTION 1, LINE 1\n'
			'SECTION 1, LINE 2\n'
			'SECTION 1, LINE 3\n'
			'== END ==' )
		self.assertEqual(result[0], expected)
		expected = (
			'== START ==\n'
			'SECTION 2, LINE 2\n'
			'== END ==' )
		self.assertEqual(result[1], expected)

	def test_find_sections_NoTrailingNewline(self):
		"""
		For fine_sections(), verifies omission of
		trailing newline does not break
		final section.
		"""
		content = (
			'Ignore Leading\n'
			'== START ==\n'
			'SECTION 1, LINE 1\n'
			'SECTION 1, LINE 2\n'
			'== END ==' )
		result = find_sections(content, re.compile('== START =='), re.compile('== END =='))

		self.assertEqual(len(result), 1)
		expected = (
			'== START ==\n'
			'SECTION 1, LINE 1\n'
			'SECTION 1, LINE 2\n'
			'== END ==' )
		self.assertEqual(result[0], expected)

	def test_simple_pattern_to_regex(self):
		"""
		Verifies basic function of simple_pattern_to_regex()
		"""
		pattern = simple_pattern_to_regex('abc*def*ghi')
		candidates = {
			'abcdefghi': True,
			'abc0def0ghi': True,
			'abc  def  ghi': True,
			# Space leading
			' abcdefghi': False,
			# Space trailing
			'abcdefghi ': True,
			# Missing leading
			'bcdefghi': False,
			# Missing trailing
			'abcdefgh': False,
		}
		result = filter(lambda x: pattern.match(x), map(lambda x: x, candidates))
		for candidate in candidates:
			self.assertEqual(candidate in result, candidates[candidate])

if __name__ == '__main__':
    unittest.main()
