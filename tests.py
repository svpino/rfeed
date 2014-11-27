import unittest
import locale
from time import gmtime, strftime
from datetime import datetime
from rfeed import *

class BaseTestCase(unittest.TestCase):

	def _element(self, element, value, attributes = {}):
		return '<' + element + '>' + value + '</' + element + '>'

class SerializableTestCase(BaseTestCase):

	def test_date(self):
		self.assertTrue(self._element('pubDate', 'Thu, 13 Nov 2014 08:00:00 GMT') in Feed('', '', '', pubDate = datetime.datetime(2014, 11, 13, 8, 0, 0)).rss())
		self.assertTrue(self._element('pubDate', 'Mon, 01 Dec 2014 10:22:15 GMT') in Feed('', '', '', pubDate = datetime.datetime(2014, 12, 1, 10, 22, 15)).rss())

class FeedTestCase(BaseTestCase):

	def test_rss_element(self):
		rss = Feed('', '', '').rss()
		self.assertTrue('<rss' in rss)		
		self.assertTrue('version="2.0"' in rss)
		self.assertTrue('</rss>' in rss)

	def test_channel_element(self):
		rss = Feed('', '', '').rss()
		self.assertTrue('<channel>' in rss)
		self.assertTrue('</channel>' in rss)

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

	def test_optional_elements(self):
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

	def test_if_generator_not_specified_use_default_value(self):
		# I'm partially checking for the element because the value includes the version number and
		# changing it will break the test. By just doing a partial match, I make sure the test keeps
		# working in future versions as well.
		self.assertTrue(self._element('docs', 'https://github.com/svpino/rfeed/blob/master/README.md') in Feed('', '', '').rss())

	def test_if_docs_not_specified_use_default_value(self):
		self.assertTrue('<generator>rfeed v' in Feed('', '', '').rss())		

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

	def test_textinput_element(self):
		rss = Feed('', '', '', textInput = TextInput('1', '2', '3', '4')).rss()
		self.assertTrue('<textInput>' in rss)
		self.assertTrue(self._element('title', '1') in rss)
		self.assertTrue(self._element('description', '2') in rss)
		self.assertTrue(self._element('name', '3') in rss)
		self.assertTrue(self._element('link', '4') in rss)
		self.assertTrue('</textInput>' in rss)

	def test_skiphours_element(self):
		rss = Feed('', '', '', skipHours = SkipHours([0, 2, 4, 6, 8, 10])).rss()
		self.assertTrue('<skipHours>' in rss)
		self.assertTrue(self._element('hour', '0') in rss)
		self.assertTrue(self._element('hour', '2') in rss)
		self.assertTrue(self._element('hour', '4') in rss)
		self.assertTrue(self._element('hour', '6') in rss)
		self.assertTrue(self._element('hour', '8') in rss)
		self.assertTrue(self._element('hour', '10') in rss)
		self.assertTrue('</skipHours>' in rss)

	def test_skipdays_element(self):
		rss = Feed('', '', '', skipDays = SkipDays(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Friday'])).rss()
		self.assertTrue('<skipDays>' in rss)
		self.assertTrue(self._element('day', 'Monday') in rss)
		self.assertTrue(self._element('day', 'Tuesday') in rss)
		self.assertTrue(self._element('day', 'Wednesday') in rss)
		self.assertTrue(self._element('day', 'Thursday') in rss)
		self.assertTrue(self._element('day', 'Friday') in rss)
		self.assertTrue(self._element('day', 'Saturday') in rss)
		self.assertTrue(self._element('day', 'Friday') in rss)
		self.assertTrue('</skipDays>' in rss)

	def test_categories_as_single_category_element(self):
		rss = Feed('', '', '', categories = Category(category = '123', domain = '234')).rss()
		self.assertTrue('<category' in rss)
		self.assertTrue('domain="234"' in rss)
		self.assertTrue('>123</category>' in rss)

	def test_categories_as_single_string_element(self):
		rss = Feed('', '', '', categories = '123').rss()
		self.assertTrue(self._element('category', '123') in rss)

	def test_categories_as_category_array_element(self):
		rss = Feed('', '', '', categories = [Category('123'), Category('234'), Category('345')]).rss()
		self.assertTrue(self._element('category', '123') in rss)
		self.assertTrue(self._element('category', '234') in rss)
		self.assertTrue(self._element('category', '345') in rss)

	def test_categories_as_string_array_element(self):
		rss = Feed('', '', '', categories = ['123', '234', '345']).rss()
		self.assertTrue(self._element('category', '123') in rss)
		self.assertTrue(self._element('category', '234') in rss)
		self.assertTrue(self._element('category', '345') in rss)

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

	def test_textinput_required_elements_validation(self):
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

	def test_skiphours_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			SkipHours(hours = None)
		self.assertTrue('hours' in str(cm.exception))

	def test_skipdays_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			SkipDays(days = None)
		self.assertTrue('days' in str(cm.exception))

	def test_enclosure_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Enclosure(url = None, length = 123, type = '')
		self.assertTrue('url' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Enclosure(url = '', length = None, type = '')
		self.assertTrue('length' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Enclosure(url = '', length = 123, type = None)
		self.assertTrue('type' in str(cm.exception))

	def test_cloud_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Cloud(domain = None, port = '', path = '', registerProcedure = '', protocol = '')
		self.assertTrue('domain' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Cloud(domain = '', port = None, path = '', registerProcedure = '', protocol = '')
		self.assertTrue('port' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Cloud(domain = '', port = '', path = None, registerProcedure = '', protocol = '')
		self.assertTrue('path' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Cloud(domain = '', port = '', path = '', registerProcedure = None, protocol = '')
		self.assertTrue('registerProcedure' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Cloud(domain = '', port = '', path = '', registerProcedure = '', protocol = None)
		self.assertTrue('protocol' in str(cm.exception))

	def test_category_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Category(category = None)
		self.assertTrue('category' in str(cm.exception))

	def test_add_extension(self):
		feed = Feed('', '', '')
		self.assertEquals(0, len(feed.extensions))
		feed.add_extension(MockExtension1())
		self.assertEquals(1, len(feed.extensions))

	def test_add_extension_raises_error_if_extension_is_not_serializable(self):
		feed = Feed('', '', '')
		with self.assertRaises(TypeError) as cm:
			feed.add_extension(Fake())

	def test_get_attributes_should_include_namespaces(self):
		self.assertTrue('name="value"' in Feed('', '', '', extensions = [MockExtension1()]).rss())

	def test_get_attributes_should_work_fine_with_no_namespaces(self):
		self.assertTrue('version="2.0"' in Feed('', '', '', extensions = [MockExtension2()]).rss())

class ItemTestCase(BaseTestCase):

	def test_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Item()
		self.assertTrue('title' in str(cm.exception))
		self.assertTrue('description' in str(cm.exception))

	def test_optional_elements(self):
		self.assertTrue(self._element('title', '123') in Feed('', '', '', items = [Item(title='123')]).rss())
		self.assertTrue(self._element('link', '123') in Feed('', '', '', items = [Item(title = '', link='123')]).rss())
		self.assertTrue(self._element('description', '123') in Feed('', '', '', items = [Item(description='123')]).rss())
		self.assertTrue(self._element('author', '123') in Feed('', '', '', items = [Item(title = '', author='123')]).rss())
		self.assertTrue(self._element('comments', '123') in Feed('', '', '', items = [Item(title = '', comments='123')]).rss())
		self.assertTrue(self._element('pubDate', 'Thu, 13 Nov 2014 08:00:00 GMT') in Feed('', '', '', items = [Item(title = '', pubDate = datetime.datetime(2014, 11, 13, 8, 0, 0))]).rss())

	def test_categories_as_single_category_element(self):
		rss = Feed('', '', '', items = [Item(title='abc', categories = Category('123', domain = '234'))]).rss()
		self.assertTrue('<category' in rss)
		self.assertTrue('domain="234"' in rss)
		self.assertTrue('>123</category>' in rss)

	def test_categories_as_single_string_element(self):
		rss = Feed('', '', '', items = [Item(title='abc', categories = '123')]).rss()
		self.assertTrue(self._element('category', '123') in rss)

	def test_categories_as_category_array_element(self):
		rss = Feed('', '', '', items = [Item(title='abc', categories = [Category('123'), Category('234'), Category('345')])]).rss()
		self.assertTrue(self._element('category', '123') in rss)
		self.assertTrue(self._element('category', '234') in rss)
		self.assertTrue(self._element('category', '345') in rss)

	def test_categories_as_string_array_element(self):
		rss = Feed('', '', '', items = [Item(title='abc', categories = ['123', '234', '345'])]).rss()
		self.assertTrue(self._element('category', '123') in rss)
		self.assertTrue(self._element('category', '234') in rss)
		self.assertTrue(self._element('category', '345') in rss)

	def test_enclosure_element(self):
		rss = Feed('', '', '', items = [Item(title = '', enclosure = Enclosure(url = '123', length = 234, type = '345'))]).rss()
		self.assertTrue('<enclosure ' in rss)
		self.assertTrue('url="123"' in rss)
		self.assertTrue('length="234"' in rss)
		self.assertTrue('type="345"' in rss)
		self.assertTrue('</enclosure>' in rss)

	def test_guid_element(self):
		rss = Feed('', '', '', items = [Item(title = '', guid = Guid(guid = '123', isPermaLink = False))]).rss()
		self.assertTrue('<guid ' in rss)
		self.assertTrue('isPermaLink="false"' in rss)
		self.assertTrue('123</guid>' in rss)

	def test_source_element(self):
		rss = Feed('', '', '', items = [Item(title = '', source = Source(name = '123', url = '234'))]).rss()
		self.assertTrue('<source ' in rss)
		self.assertTrue('url="234"' in rss)
		self.assertTrue('123</source>' in rss)

	def test_guid_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Guid(guid = None)
		self.assertTrue('guid' in str(cm.exception))

	def test_source_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Source(name = None, url = '123')
		self.assertTrue('name' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Source(name = '123', url = None)
		self.assertTrue('url' in str(cm.exception))

	def test_guid_ispermalink_should_be_true_by_default(self):
		guid = Guid(guid = '123')
		self.assertTrue(guid.isPermaLink)

	def test_guid_ispermalink_should_be_true_if_none_is_provided(self):
		guid = Guid(guid = '123', isPermaLink = None)
		self.assertTrue(guid.isPermaLink)

class iTunesTestCase(BaseTestCase):

	def test_namespace_is_added_to_the_feed(self):
		self.assertTrue('xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"' in Feed('', '', '', extensions = [iTunes()]).rss())

	def test_optional_elements(self):
		self.assertTrue(self._element('itunes:author', 'svpino') in Feed('', '', '', extensions = [iTunes(author = 'svpino')]).rss())
		self.assertTrue(self._element('itunes:subtitle', '123') in Feed('', '', '', extensions = [iTunes(subtitle = '123')]).rss())
		self.assertTrue(self._element('itunes:summary', '123') in Feed('', '', '', extensions = [iTunes(summary = '123')]).rss())

	def test_block_can_be_specified_as_boolean(self):
		self.assertTrue(self._element('itunes:block', 'yes') in Feed('', '', '', extensions = [iTunes(block = True)]).rss())
		self.assertTrue(self._element('itunes:block', 'no') in Feed('', '', '', extensions = [iTunes(block = False)]).rss())

	def test_block_can_be_specified_as_string(self):
		self.assertTrue(self._element('itunes:block', 'yes') in Feed('', '', '', extensions = [iTunes(block = 'yes')]).rss())
		self.assertTrue(self._element('itunes:block', 'yes') in Feed('', '', '', extensions = [iTunes(block = 'YES')]).rss())
		self.assertTrue(self._element('itunes:block', 'no') in Feed('', '', '', extensions = [iTunes(block = 'xyz')]).rss())

	def test_image_element(self):
		self.assertTrue('<itunes:image href="123"></itunes:image>' in Feed('', '', '', extensions = [iTunes(image = '123')]).rss())

	def test_complete_can_be_specified_as_boolean(self):
		self.assertTrue(self._element('itunes:complete', 'yes') in Feed('', '', '', extensions = [iTunes(complete = True)]).rss())
		self.assertTrue(self._element('itunes:complete', 'no') in Feed('', '', '', extensions = [iTunes(complete = False)]).rss())

	def test_complete_can_be_specified_as_string(self):
		self.assertTrue(self._element('itunes:complete', 'yes') in Feed('', '', '', extensions = [iTunes(complete = 'yes')]).rss())
		self.assertTrue(self._element('itunes:complete', 'yes') in Feed('', '', '', extensions = [iTunes(complete = 'YES')]).rss())
		self.assertTrue(self._element('itunes:complete', 'no') in Feed('', '', '', extensions = [iTunes(complete = 'xyz')]).rss())

	def test_explicit_can_be_specified_as_boolean(self):
		self.assertTrue(self._element('itunes:explicit', 'yes') in Feed('', '', '', extensions = [iTunes(explicit = True)]).rss())
		self.assertTrue(self._element('itunes:explicit', 'clean') in Feed('', '', '', extensions = [iTunes(explicit = False)]).rss())

	def test_explicit_can_be_specified_as_string(self):
		self.assertTrue(self._element('itunes:explicit', 'yes') in Feed('', '', '', extensions = [iTunes(explicit = 'yes')]).rss())
		self.assertTrue(self._element('itunes:explicit', 'yes') in Feed('', '', '', extensions = [iTunes(explicit = 'YES')]).rss())
		self.assertTrue(self._element('itunes:explicit', 'clean') in Feed('', '', '', extensions = [iTunes(explicit = 'xyz')]).rss())

	def test_explicit_should_not_be_included_if_not_specified(self):
		self.assertFalse(self._element('itunes:explicit', 'yes') in Feed('', '', '', extensions = [iTunes()]).rss())
		self.assertFalse(self._element('itunes:explicit', 'clean') in Feed('', '', '', extensions = [iTunes()]).rss())

	def test_owner_required_elements_validation(self):
		with self.assertRaises(ElementRequiredError) as cm:
			Owner(name = None, email = '')
		self.assertTrue('name' in str(cm.exception))

		with self.assertRaises(ElementRequiredError) as cm:
			Owner(name = '', email = None)
		self.assertTrue('email' in str(cm.exception))

	def test_owner_element(self):
		rss = Feed('', '', '', extensions = [iTunes(owner = Owner('123', '234'))]).rss()
		self.assertTrue('<itunes:owner>' in rss)
		self.assertTrue(self._element('itunes:name', '123') in rss)
		self.assertTrue(self._element('itunes:email', '234') in rss)
		self.assertTrue('</itunes:owner>' in rss)


class MockExtension1(Extension):
	def __init__(self):
		Extension.__init__(self)

	def get_namespace(self):
		return {"name": "value"}

	def _publish(self, handler):
		Extension._publish(self, handler)

class MockExtension2(Extension):
	def __init__(self):
		Extension.__init__(self)

	def _publish(self, handler):
		Extension._publish(self, handler)

class Fake:
	pass

if __name__ == '__main__':
    unittest.main()