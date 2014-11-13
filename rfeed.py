import sys
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
	def __init__(self, title, link, description, language = None, copyright = None, managingEditor = None, webMaster = None, items = None):
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

		for item in self.items:
			item.handler = self.handler
			item._publish()

class ElementRequiredError(Exception):
    def __init__(self, element):
        self.element = element

    def __str__(self):
        return 'The element "' + self.element + '" is required and can\'t be None'
