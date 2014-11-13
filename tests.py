import unittest
from rfeed import *

class FeedTestCase(unittest.TestCase):

	def test_required_elements(self):
		self.assertTrue(self._element('title', 'This is a sample title') in Feed('This is a sample title', '', '').rss())
		self.assertTrue(self._element('link', 'https://rfeed.svpino.com') in Feed('', 'https://rfeed.svpino.com', '').rss())
		self.assertTrue(self._element('description', 'This is a sample description') in Feed('', '', 'This is a sample description').rss())

	def test_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Feed(title = None, link = '', description = '')
		self.assertTrue('title' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Feed(title = '', link = None, description = '')
		self.assertTrue('link' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Feed(title = '', link = '', description = None)
		self.assertTrue('description' in str(cm.exception))

	def test_optional_elements_are_present(self):
		self.assertTrue(self._element('language', 'en-us') in Feed('', '', '', language = 'en-us').rss())
		self.assertTrue(self._element('copyright', 'Copyright 2014') in Feed('', '', '', copyright = 'Copyright 2014').rss())
		self.assertTrue(self._element('managingEditor', 'John Doe') in Feed('', '', '', managingEditor = 'John Doe').rss())
		self.assertTrue(self._element('webMaster', 'john@doe.com') in Feed('', '', '', webMaster = 'john@doe.com').rss())

	def test_optional_elements_are_abscent(self):
		rss = Feed('title', 'link', 'description').rss()
		self.assertFalse('language' in rss)
		self.assertFalse('copyright' in rss)
		self.assertFalse('managingEditor' in rss)
		self.assertFalse('webMaster' in rss)

	def _element(self, element, value):
		return '<' + element + '>' + value + '</' + element + '>'

if __name__ == '__main__':
    unittest.main()