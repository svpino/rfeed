import sys
from StringIO import StringIO
from xml.sax import saxutils

class Serializable:
	def __init__(self):
		self.handler = None

	def _write_element(self, name, value, attributes = {}):
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
	def __init__(self, title, items = None):
		Serializable.__init__(self)

		self.title = title
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

		for item in self.items:
			item.handler = self.handler
			item._publish()

if __name__ == '__main__':
	item1 = Item("Title 1")
	item2 = Item("Title 2")
	feed = Feed("En 3 y 2", [item1, item2])
	print feed.rss()