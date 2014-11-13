__name__ = "rfeed"
__version__ = (1, 0, 0)
__author__ = "Santiago L. Valdarrama - https://blog.svpino.com"
_generator = __name__ + " v" + ".".join(map(str, __version__))

import sys
import datetime
from StringIO import StringIO
from xml.sax import saxutils

class Serializable:
	def __init__(self):
		self.handler = None

	def _write_element(self, name, value, attributes = {}):
		if value is not None:
			self.handler.startElement(name, attributes)
			self.handler.characters(value)
			self.handler.endElement(name)

	def _publish(self):
		# This is the method that subclasses should override
		pass

	def date(self, date):
		""" Converts a datetime into an RFC 822 formatted date.
		This method assumes that the input date is in GMT.
		Returns None if None is provided as an argument.
		"""

		# Alright, I admit it: this method looks hideous. The thing is that RFC 822 requires a specific format for dates, and strftime is 
		# locale dependent, so I can't use it to create the final date unless I force change the system locale.
		#
		# I looked into that (locale.setlocale, then restore), but I got the feeling that I was doing things that I was going to regret later.
		# Maybe it's just me, but it doesn't feel right to force change the locale just to create a simple date.
		#
		# So, not having a better solution, I went ahead and used the original method from the PyRSS2Gen library.

		if date is None:
			return None
		
		return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][date.weekday()], date.day,
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][date.month-1], date.year, date.hour, date.minute, date.second)

class iTunes(Serializable):
	def __init__(self, author, block, category, image, explicit, complete, new_feed_url, owner, subtitle, summary):
		Serializable.__init__(self)

		self.author = author
		self.block = block
		self.category = category
		self.image = image
		self.explicit = explicit
		self.complete = complete
		self.new_feed_url = new_feed_url
		self.owner = owner
		self.subtitle = subtitle
		self.summary = summary

class Item(Serializable):
	def __init__(self, title):
		Serializable.__init__(self)

		self.title = title

	def _publish(self):
		self.handler.startElement("item", {})

		self._write_element("title", self.title)

		self.handler.endElement("item")

class Feed(Serializable):
	def __init__(self, 
		title, 						# The name of the channel.
		link, 						# The URL to the HTML website corresponding to the channel.
		description, 				# Phrase or sentence describing the channel.
		language = None, 			# The language the channel is written in.
		copyright = None, 			# Copyright notice for content in the channel.
		managingEditor = None, 		# Email address for person responsible for editorial content.
		webMaster = None, 			# Email address for person responsible for technical issues relating to channel.
		pubDate = None,				# The publication date for the content in the channel. This should be a datetime in GMT format.
		lastBuildDate = None,		# The last time the content of the channel changed. This should be a datetime in GMT format.
		generator = None,			# A string indicating the program used to generate the channel.

		items = None):

		Serializable.__init__(self)

		if title is None: raise ElementRequiredError("title")
		if link is None: raise ElementRequiredError("link")
		if description is None: raise ElementRequiredError("description")

		self.title = title
		self.link = link
		self.description = description
		self.language = language
		self.copyright = copyright
		self.managingEditor = managingEditor
		self.webMaster = webMaster
		self.pubDate = pubDate
		self.lastBuildDate = lastBuildDate

		self.generator = _generator if generator is None else generator

		self.items = [] if items is None else items

	def rss(self):
		output = StringIO()
		self.handler = saxutils.XMLGenerator(output, 'iso-8859-1')
		self.handler.startDocument()
		self._publish()
		self.handler.endDocument()
		return output.getvalue()

	def _publish(self):
		self._write_element("title", self.title)
		self._write_element("link", self.link)
		self._write_element("description", self.description)
		self._write_element("language", self.language)
		self._write_element("copyright", self.copyright)
		self._write_element("managingEditor", self.managingEditor)
		self._write_element("webMaster", self.webMaster)
		self._write_element("pubDate", self.date(self.pubDate))
		self._write_element("lastBuildDate", self.date(self.lastBuildDate))
		self._write_element("generator", self.generator)

		for item in self.items:
			item.handler = self.handler
			item._publish()

class ElementRequiredError(Exception):
    def __init__(self, element):
        self.element = element

    def __str__(self):
        return 'The element "' + self.element + '" is required and can\'t be None'
