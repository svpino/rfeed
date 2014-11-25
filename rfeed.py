__name__ = "rfeed"
__version__ = (1, 0, 0)
__author__ = "Santiago L. Valdarrama - https://blog.svpino.com"
_generator = __name__ + " v" + ".".join(map(str, __version__))
_docs = "https://github.com/svpino/rfeed/blob/master/README.md"

import sys
import datetime
from StringIO import StringIO
from xml.sax import saxutils

class Serializable:
	def __init__(self):
		self.handler = None

	def _write_element(self, name, value, attributes = {}):
		if value is not None or attributes != {}:
			self.handler.startElement(name, attributes)

			if value is not None:
				self.handler.characters(str(value))

			self.handler.endElement(name)

	def _publish(self, handler):
		self.handler = handler

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

class Category(Serializable):
	""" A Category object specify one or more categories that the channel or item belongs to.
	More information at http://cyber.law.harvard.edu/rss/rss.html#ltcategorygtSubelementOfLtitemgt
	"""
	def __init__(self, category, domain = None):
		""" Keyword arguments:
		category --	The name of the category
		domain -- Optional. A string that identifies a categorization taxonomy. 
		"""

		Serializable.__init__(self)

		if category is None: raise ElementRequiredError("category")

		self.category = category
		self.domain = domain

	def _publish(self, handler):
		Serializable._publish(self, handler)
		
		self._write_element("category", self.category, { "domain": self.domain } if self.domain is not None else {})

class Cloud(Serializable):
	""" A Cloud object specifies a web service that supports the rssCloud interface which can be implemented in HTTP-POST, XML-RPC or SOAP 1.1. 
	More information at http://cyber.law.harvard.edu/rss/rss.html#ltcloudgtSubelementOfLtchannelgt
	"""
	def __init__(self, domain, port, path, registerProcedure, protocol):
		""" Keyword arguments:
		domain -- The domain name or IP address of the cloud. 
		port --	TCP port that the cloud is running on.
		path -- The location of its responder.
		registerProcedure -- The name of the procedure to call to request notification.
		protocol -- Indication of which protocol is to be used.
		"""

		Serializable.__init__(self)

		if domain is None: raise ElementRequiredError("domain")
		if port is None: raise ElementRequiredError("port")
		if path is None: raise ElementRequiredError("path")
		if registerProcedure is None: raise ElementRequiredError("registerProcedure")
		if protocol is None: raise ElementRequiredError("protocol")

		self.domain = domain
		self.port = port
		self.path = path
		self.registerProcedure = registerProcedure
		self.protocol = protocol

	def _publish(self, handler):
		Serializable._publish(self, handler)		

		self._write_element("cloud", None, { "domain": self.domain, "port": str(self.port), "path": self.path, "registerProcedure": self.registerProcedure, "protocol": self.protocol })

class Image(Serializable):
	""" An Image object specifies a GIF, JPEG or PNG image that can be displayed with the channel.
	More information at http://cyber.law.harvard.edu/rss/rss.html#ltimagegtSubelementOfLtchannelgt
	"""
	def __init__(self, url, title, link, width = None, height = None, description = None):	
		""" Keyword arguments:
		url -- The URL of the image that represents the channel. 
    	title -- Describes the image. It's used in the ALT attribute of the HTML <img> tag when the channel is rendered in HTML. 
    	link -- The URL of the site. When the channel is rendered the image is a link to the site.
    	width -- Optional. The width of the image in pixels.
    	height -- Optional. The height of the image in pixels.
    	description -- Optional. Contains text that is included in the TITLE attribute of the link formed around the image in the HTML rendering.
		"""

		Serializable.__init__(self)

		if url is None: raise ElementRequiredError("url")
		if title is None: raise ElementRequiredError("title")
		if link is None: raise ElementRequiredError("link")

		self.url = url
		self.title = title
		self.link = link
		self.width = width
		self.height = height
		self.description = description
        
	def _publish(self, handler):
		Serializable._publish(self, handler)
		self.handler.startElement("image", {})

		self._write_element("url", self.url)
		self._write_element("title", self.title)
		self._write_element("link", self.link)
		self._write_element("width", self.width)
		self._write_element("height", self.height)
		self._write_element("description", self.description)

		self.handler.endElement("image")

class TextInput(Serializable):
	""" A TextInput object specifies a text input box that can be displayed with the channel.
	More information at http://cyber.law.harvard.edu/rss/rss.html#lttextinputgtSubelementOfLtchannelgt
	"""
	def __init__(self, title, description, name, link):
		""" Keyword arguments:
		title -- The label of the submit button in the text input area. 
		description -- Explains the text input area.
		name -- The name of the text object in the text input area. 
		link -- The URL of the CGI script that processes text input requests. 
		"""

		Serializable.__init__(self)

		if title is None: raise ElementRequiredError("title")
		if description is None: raise ElementRequiredError("description")
		if name is None: raise ElementRequiredError("name")
		if link is None: raise ElementRequiredError("link")

		self.title = title
		self.description = description
		self.name = name
		self.link = link

	def _publish(self, handler):
		Serializable._publish(self, handler)
		self.handler.startElement("textInput", {})

		self._write_element("title", self.title)
		self._write_element("description", self.description)
		self._write_element("name", self.name)
		self._write_element("link", self.link)

		self.handler.endElement("textInput")

class SkipHours(Serializable):
	""" A SkipHours object is a hint for aggregators telling them which hours they can skip.
	More information at http://cyber.law.harvard.edu/rss/skipHoursDays.html#skiphours
	"""
	def __init__(self, hours):
		""" Keyword arguments:
		hours -- A list containing up to 24 values between 0 and 23, representing a time in GMT.
		"""

		Serializable.__init__(self)

		if hours is None: raise ElementRequiredError("hours")

		self.hours = hours

	def _publish(self, handler):
		Serializable._publish(self, handler)

		if self.hours:
			self.handler.startElement("skipHours", {})

			for hour in self.hours:
				self._write_element("hour", hour)

			self.handler.endElement("skipHours")

class SkipDays(Serializable):
	""" A SkipDays object is a hint for aggregators telling them which days they can skip.
	More information at http://cyber.law.harvard.edu/rss/skipHoursDays.html#skipdays
	"""
	def __init__(self, days):
		""" Keyword arguments:
		days -- A list containing up to 7 values. Possible values are Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.
		"""

		Serializable.__init__(self)

		if days is None: raise ElementRequiredError("days")

		self.days = days

	def _publish(self, handler):
		Serializable._publish(self, handler)

		if self.days:
			self.handler.startElement("skipDays", {})

			for day in self.days:
				self._write_element("day", day)

			self.handler.endElement("skipDays")

class Enclosure(Serializable):
	""" An Enclosure object describes a media object that is attached to the item.
	More information at http://cyber.law.harvard.edu/rss/rss.html#ltenclosuregtSubelementOfLtitemgt
	"""
	def __init__(self, url, length, type):
		""" Keyword arguments:
		url -- Indicates where the enclosure is located.
		length -- Specifies how big the enclosure is in bytes.
		type -- Specifies the standard MIME type of the enclosure.
		"""
		Serializable.__init__(self)

		if url is None: raise ElementRequiredError("url")
		if length is None: raise ElementRequiredError("length")
		if type is None: raise ElementRequiredError("type")

		self.url = url
		self.length = length
		self.type = type

	def _publish(self, handler):
		Serializable._publish(self, handler)

		self._write_element("enclosure", None, { "url": self.url, "length": str(self.length), "type": self.type })

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
	""" An Item object may represent a "story" - much like a story in a newspaper or magazine; if so its description is a synopsis of the story, and the link points to the full story. 
	An item may also be complete in itself, if so, the description contains the text, and the link and title may be omitted. All elements of an item are optional, however at least one 
	of title or description must be present.
	More information at http://cyber.law.harvard.edu/rss/rss.html#hrelementsOfLtitemgt
	"""
	def __init__(self, title = None, link = None, description = None, author = None, categories = None, comments = None, enclosure = None, guid = None, pubDate = None, source = None):
		""" Keyword arguments:
		title -- Optional. The title of the item.
		link  -- Optional. The URL of the item.
		description -- Optional. The item synopsis.
		author -- Optional. Email address of the author of the item.
		categories -- Optional. Includes the item in one or more categories.
		comments -- Optional. URL of a page for comments relating to the item.
		enclosure -- Optional. Describes a media object that is attached to the item.
		guid -- Optional. A string that uniquely identifies the item.
		pubDate -- Optional. Indicates when the item was published.
		source -- Optional. The RSS channel that the item came from.
		"""

		Serializable.__init__(self)

		if title is None and description is None:
			raise ElementRequiredError("title", "description")

		self.title = title
		self.link = link
		self.description = description
		self.author = author
		self.comments = comments
		self.enclosure = enclosure
		self.guid = guid
		self.pubDate = pubDate
		self.source = source

		self.categories = [] if categories is None else categories

		if isinstance(self.categories, Category):
			self.categories = [self.categories]
		elif isinstance(self.categories, basestring):
			self.categories = [Category(self.categories)]

	def _publish(self, handler):
		Serializable._publish(self, handler)

		self.handler.startElement("item", {})

		self._write_element("title", self.title)
		self._write_element("link", self.link)
		self._write_element("description", self.description)
		self._write_element("author", self.author)
		self._write_element("comments", self.comments)

		for category in self.categories:
			if isinstance(category, basestring):
				category = Category(category)
			category._publish(self.handler)

		if self.enclosure is not None:
			self.enclosure._publish(self.handler)

		self.handler.endElement("item")


class Feed(Serializable):
	def __init__(self, title, link, description, language = None, copyright = None, managingEditor = None, webMaster = None, pubDate = None, lastBuildDate = None, categories = None, 
		generator = None, docs = None, cloud = None, ttl = None, image = None, rating = None, textInput = None, skipHours = None, skipDays = None, items = None):
		""" Keyword arguments:
		title -- The name of the channel.
		link -- The URL to the HTML website corresponding to the channel.
		description -- Phrase or sentence describing the channel.
		language -- Optional. The language the channel is written in.
		copyright -- Optional. Copyright notice for content in the channel.
		managingEditor -- Optional. Email address for person responsible for editorial content.
		webMaster -- Optional. Email address for person responsible for technical issues relating to channel.
		pubDate -- Optional. The publication date for the content in the channel. This should be a datetime in GMT format.
		lastBuildDate -- Optional. The last time the content of the channel changed. This should be a datetime in GMT format.
		categories -- Optional. Specify one or more categories that the channel belongs to.
		generator -- Optional. A string indicating the program used to generate the channel.
		docs -- Optional. A URL that points to the documentation for the format used in the RSS file.
		cloud -- Optional. Allows processes to register with a cloud to be notified of updates to the channel. This is a Cloud object.
		ttl -- Optional. The number of minutes that indicates how long a channel can be cached before refreshing from the source. This should be an integer value.
		image -- Optional. Specifies an image that can be displayed with the channel. This is an Image object.
		rating -- Optional. The PICS rating for the channel. See http://www.w3.org/PICS/.
		textInput -- Optional. Specifies a text input box that can be displayed with the channel.
		skipHours -- Optional. A hint for aggregators telling them which hours they can skip.
		skipDays -- Optional. A hint for aggregators telling them which days they can skip.
		"""

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
		self.docs = _docs if docs is None else docs
		self.cloud = cloud
		self.ttl = ttl
		self.image = image
		self.rating = rating
		self.textInput = textInput 
		self.skipHours = skipHours
		self.skipDays = skipDays

		self.categories = [] if categories is None else categories

		if isinstance(self.categories, Category):
			self.categories = [self.categories]
		elif isinstance(self.categories, basestring):
			self.categories = [Category(self.categories)]

		self.items = [] if items is None else items

	def rss(self):
		output = StringIO()
		handler = saxutils.XMLGenerator(output, 'iso-8859-1')
		handler.startDocument()
		self._publish(handler)
		handler.endDocument()
		return output.getvalue()

	def _publish(self, handler):
		Serializable._publish(self, handler)

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
		self._write_element("docs", self.docs)
		self._write_element("ttl", self.ttl)
		self._write_element("rating", self.rating)

		for category in self.categories:
			if isinstance(category, basestring):
				category = Category(category)
			category._publish(self.handler)

		if self.cloud is not None:
			self.cloud._publish(self.handler)

		if self.image is not None:
			self.image._publish(self.handler)

		if self.textInput is not None:
			self.textInput._publish(self.handler)

		if self.skipHours is not None:
			self.skipHours._publish(self.handler)

		if self.skipDays is not None:
			self.skipDays._publish(self.handler)	

		for item in self.items:
			item._publish(self.handler)

class ElementRequiredError(Exception):
    def __init__(self, element1, element2 = None):
        self.element1 = element1
        self.element2 = element2

    def __str__(self):
		if self.element2 is not None:
			return 'Either "' + self.element1 + '" or "' + self.element2 + '" must be defined'	

		return '"' + self.element1 + '" must be defined'

