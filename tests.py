import unittest
import locale
from time import gmtime, strftime
from datetime import datetime
from rfeed import *

class SerializableTestCase(unittest.TestCase):

	def test_date(self):
		self.assertEquals('Thu, 13 Nov 2014 08:00:00 GMT', Serializable().date(datetime.datetime(2014, 11, 13, 8, 0, 0)))
		self.assertEquals('Mon, 01 Dec 2014 10:22:15 GMT', Serializable().date(datetime.datetime(2014, 12, 1, 10, 22, 15)))

	def test_date_returns_none_if_date_is_none(self):
		self.assertIsNone(Serializable().date(None))

class FeedTestCase(unittest.TestCase):

	def test_required_elements(self):

		self.assertTrue(self._element('title', 'This is a sample title') in Feed('This is a sample title', '', '').rss())
		self.assertTrue(self._element('link', 'https://www.google.com') in Feed('', 'https://www.google.com', '').rss())
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
		self.assertTrue(self._element('pubDate', 'Thu, 13 Nov 2014 08:00:00 GMT') in Feed('', '', '', pubDate = datetime.datetime(2014, 11, 13, 8, 0, 0)).rss())
		self.assertTrue(self._element('lastBuildDate', 'Mon, 01 Dec 2014 10:22:15 GMT') in Feed('', '', '', lastBuildDate = datetime.datetime(2014, 12, 1, 10, 22, 15)).rss())
		self.assertTrue(self._element('generator', 'Generator goes here') in Feed('', '', '', generator = 'Generator goes here').rss())
		self.assertTrue(self._element('docs', 'Docs goes here') in Feed('', '', '', docs = 'Docs goes here').rss())
		self.assertTrue(self._element('ttl', '123') in Feed('', '', '', ttl = 123).rss())
		self.assertTrue(self._element('rating', 'abc') in Feed('', '', '', rating = 'abc').rss())

	def test_cloud_element(self):
		rss = Feed('', '', '', cloud = Cloud('1', 2, '3', '4', '5')).rss()
		self.assertTrue('<cloud ' in rss)
		self.assertTrue('domain="1"' in rss)
		self.assertTrue('port="2"' in rss)
		self.assertTrue('path="3"' in rss)
		self.assertTrue('registerProcedure="4"' in rss)
		self.assertTrue('protocol="5"' in rss)
		self.assertTrue('</cloud>' in rss)

	def test_image_element(self):
		rss = Feed('', '', '', image = Image('1', '2', '3', 4, 5, '6')).rss()
		self.assertTrue('<image>' in rss)
		self.assertTrue(self._element('url', '1') in rss)
		self.assertTrue(self._element('title', '2') in rss)
		self.assertTrue(self._element('link', '3') in rss)
		self.assertTrue(self._element('width', '4') in rss)
		self.assertTrue(self._element('height', '5') in rss)
		self.assertTrue(self._element('description', '6') in rss)
		self.assertTrue('</image>' in rss)

	def test_image_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Image(url = None, title = '', link = '')
		self.assertTrue('url' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Image(url = '', title = None, link = '')
		self.assertTrue('title' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Image(url = '', title = '', link = None)
		self.assertTrue('link' in str(cm.exception))

	def test_textInput_element(self):
		rss = Feed('', '', '', textInput = TextInput('1', '2', '3', '4')).rss()
		self.assertTrue('<textInput>' in rss)
		self.assertTrue(self._element('title', '1') in rss)
		self.assertTrue(self._element('description', '2') in rss)
		self.assertTrue(self._element('name', '3') in rss)
		self.assertTrue(self._element('link', '4') in rss)
		self.assertTrue('</textInput>' in rss)

	def test_textInput_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			TextInput(title = None, description = '', name = '', link = '')
		self.assertTrue('title' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			TextInput(title = '', description = None, name = '', link = '')
		self.assertTrue('description' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			TextInput(title = '', description = '', name = None, link = '')
		self.assertTrue('name' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			TextInput(title = '', description = '', name = '', link = None)
		self.assertTrue('link' in str(cm.exception))

	def test_skipHours_element(self):
		rss = Feed('', '', '', skipHours = SkipHours([0, 2, 4, 6, 8, 10])).rss()
		self.assertTrue('<skipHours>' in rss)
		self.assertTrue(self._element('hour', '0') in rss)
		self.assertTrue(self._element('hour', '2') in rss)
		self.assertTrue(self._element('hour', '4') in rss)
		self.assertTrue(self._element('hour', '6') in rss)
		self.assertTrue(self._element('hour', '8') in rss)
		self.assertTrue(self._element('hour', '10') in rss)
		self.assertTrue('</skipHours>' in rss)

	def test_if_generator_not_specified_use_default_value(self):
		# I'm partially checking for the element because the value includes the version number and
		# changing it will break the test. By just doing a partial match, I make sure the test keeps
		# working in future versions as well.
		self.assertTrue(self._element('docs', 'https://github.com/svpino/rfeed/blob/master/README.md') in Feed('', '', '').rss())

	def test_if_docs_not_specified_use_default_value(self):
		self.assertTrue('<generator>rfeed v' in Feed('', '', '').rss())		

	def _element(self, element, value, attributes = {}):

		return '<' + element + '>' + value + '</' + element + '>'

if __name__ == '__main__':
    unittest.main()