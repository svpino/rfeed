## Overview

**rfeed** is a library to generate RSS 2.0 feeds in Python. It's based on the work from Andrew Dalke in the 
[PyRSS2Gen](http://www.dalkescientific.com/Python/PyRSS2Gen.html) library (see the [Inspiration](https://github.com/svpino/rfeed/blob/master/README.md#inspiration) 
section below for more information.)

**rfeed** is extensible, and in my opinion very easy to use. Besides the standard RSS 2.0 specification, it also includes
[iTunes](https://www.apple.com/itunes/podcasts/specs.html) support for podcast feeds.

## Installation

The library is a single file `rfeed.py`, so you could simply copy it wherever you need it. You can also install it using the 
following command:
	
	% python setup.py install

## Usage

I don't think you are going to find a better reference for using the library than the test suite in `tests.py`. However, unit tests 
are sometimes hard to understand and isolated, so here is a simple example from end to end:

```python
import datetime 
from rfeed import *

item1 = Item(
	title = "First article",
	link = "http://www.example.com/articles/1", 
	description = "This is the description of the first article",
    author = "Santiago L. Valdarrama",
    guid = Guid("http://www.example.com/articles/1"),
	pubDate = datetime.datetime(2014, 12, 29, 10, 00))

item2 = Item(
	title = "Second article",
	link = "http://www.example.com/articles/2", 
	description = "This is the description of the second article",
    author = "Santiago L. Valdarrama",
    guid = Guid("http://www.example.com/articles/2"),
	pubDate = datetime.datetime(2014, 12, 30, 14, 15))

feed = Feed(
	title = "Sample RSS Feed",
	link = "http://www.example.com/rss",
	description = "This is an example of how to use rfeed to generate an RSS 2.0 feed",
	language = "en-US",
	lastBuildDate = datetime.datetime.now(),
	items = [item1, item2])

print feed.rss()	

```

It's a very succinct example, but it exposes the following concepts:

* The main object of the RSS 2.0 feed is the `Feed` class.
* The `Feed` class supports a list of `Item` instances.
* To specify the `guid` attribute of an item, you can use a `Guid` instance.
* To get the final RSS content, you can use the `rss()` method of the `Feed` class.

Of course, there's way more than what the example above illustrates. Here is the full list of exposed classes and a brief
description of each one of them:

* `Feed`: This is the main class that represents the RSS 2.0 feed. 
* `Item`: Represents an item of a feed's channel.
* `Category`: Represents one or more categories that the channel or item belongs to.
* `Cloud`: Represents a web service that supports the rssCloud interface which can be implemented in HTTP-POST, XML-RPC or SOAP 1.1. 
* `Image`: Represents a GIF, JPEG or PNG image that can be displayed with the channel.
* `TextInput`: Represents a text input box that can be displayed with the channel.
* `SkipHours`: Represents a hint for aggregators telling them which hours they can skip.
* `SkipDays`:  Represents a hint for aggregators telling them which days they can skip.
* `Enclosure`: Represents a media object that is attached to a feed's item.
* `Guid`: Represents a string that uniquely identifies the item.
* `Source`: Represents the RSS channel that the item came from.

(For more information about each one of these classes, you can check the official [RSS 2.0 specification](http://cyber.law.harvard.edu/rss/rss.html), and check 
out the `rfeed.py` source file.)

## Extending the library

The RSS 2.0 specification is extensible, so it's **rfeed**. Adding extra content to your feed is very simple:

1. Create a class that extends the `Extension` class. 
2. Overwite the `Extension.get_namespace` method to return the namespace of your extension (the one will be included in the `<rss/>` element of your feed.) 
If you don't need to add a namespace, you can simply extend the `Serializable` class instead.
3. Use the `Feed.add_extension()` method, or the `extensions` array in the constructor to provide your extension.

Here is an example of extending your feed with a `content:encoded` element:

```python
import datetime 
from rfeed import *

class Content(Extension):
	def get_namespace(self):
		return {"xmlns:content": "http://purl.org/rss/1.0/modules/content/"}

class ContentItem(Serializable):
	def __init__(self, content):
		Serializable.__init__(self)
		self.content = content

	def publish(self, handler):
		Serializable.publish(self, handler)
		self._write_element("content:encoded", self.content)

item = Item(
	title = "Sample article",
	link = "http://www.example.com/articles/1", 
	description = "This is the description of the first article",
    author = "Santiago L. Valdarrama",
    guid = Guid("http://www.example.com/articles/1"),
	pubDate = datetime.datetime(2014, 12, 29, 10, 00),
	extensions = [ContentItem('This is the value of the enconded content')])

feed = Feed(
	title = "Sample RSS Feed",
	link = "http://www.example.com/rss"
	description = "This is an example of how to use rfeed to generate an RSS 2.0 feed",
	language = "en-US",
	lastBuildDate = datetime.datetime.now(),
	items = [item],
	extensions = [Content()])

print feed.rss()	
```
* Note that we want to add our `Content` instance to the list of extensions at the feed level. This way we make sure the namespace
is included in the feed.
* In this case the `Content` instance doesn't provide a `publish` method because there's nothing to add to the `<channel/>` element 
of the feed.
* The `ContentItem` class extends `Serializable` because it doesn't need to provide a namespace (it was already provided by the `Content`
instace.)
* The `ContentItem` instance implements the `publish` method and uses the `_write_element` method to output the specific XML content.

For a more exhaustive example, check the implementation of the iTunes extension in the `rfeed.py` file.

## iTunes Support

Podcasts are a huge medium in 2014, and iTunes is the preferred way of publishing them. This is the reason **rfeed** provides an extension
for iTunes support. Here is an example of how to use it:

```python
import datetime 
from rfeed import *

 itunes_item = iTunesItem(
    author = "Santiago L. Valdarrama",
    image = "http://www.example.com/artwork.jpg",
    duration = "01:11:02",
    explicit = "clean",
    subtitle = "The subtitle of the podcast episode",
    summary = "Here is the summary of this specific episode")

item = Item(
	title = "Sample article",
	link = "http://www.example.com/articles/1", 
	description = "This is the description of the first article",
	author = "Santiago L. Valdarrama",
	guid = Guid("http://www.example.com/articles/1"),
	pubDate = datetime.datetime(2014, 12, 29, 10, 00),
	enclosure = Enclosure(url="http://www.example.com/articles/1.mp3", length=0, type=''),
	extensions = [itunes_item])

itunes = iTunes(
    author = "Santiago L. Valdarrama",
    subtitle = "A sample podcast that will never be produced",
    summary = "This is just a fake description",
    image = "http://www.example.com/artwork.jpg",
    explicit = "clean",
    categories = iTunesCategory(name = 'Technology', subcategory = 'Software How-To'),
    owner = iTunesOwner(name = 'Santiago L. Valdarrama', email = 'svpino@gmail.com'))

feed = Feed(
	title = "Sample Podcast RSS Feed",
	link = "http://www.example.com/rss",
	description = "An example of how to generate an RSS 2.0 feed",
	language = "en-US",
	lastBuildDate = datetime.datetime.now(),
	items = [item],
	extensions = [itunes])

print(feed.rss())	
```

## Inspiration

I created my own [blog](https://www.shiftedup.com) engine in Python for [Google App Engine](https://cloud.google.com/appengine/), 
thus I needed a way to generate my RSS feed. Later on, I added a podcast site that also needed an RSS 
feed, but this time with [iTunes](https://www.apple.com/itunes/podcasts/specs.html) support.

The only help I could find was the amazing [PyRSS2Gen](http://www.dalkescientific.com/Python/PyRSS2Gen.html) library written by 
Andrew Dalke. The library is very simple, but it didn't help with the iTunes support, so I found myself modifying it to get as 
much as I could out of it.

At the end I didn't like what I did to the original library: it was messy all around. It wasn't the library's fault, but my 
own. I decided to fix the problem from scratch, by rewriting the library in a different way.

I'm not claiming this new version is better than the original. It's just different and I think a little bit easier to extend and 
maintain (since it comes with a suite full of unit tests). Since I needed iTunes support from the beginning, I also coded an 
iTunes extension for the library. Now I'm powering my blog and podcast sites with it, and I hope it serves well to anyone with 
similar needs.

Thanks to Andrew Dalke for writing (what I consider) the first version a long time ago. This project is based on his original work, 
borrowing ideas and code from it, but with enough differences that I felt it deserved a new name.

## Contributing

Contributions, questions and comments are all welcome and encouraged. If you run into any problems, please submit an issue and I'll
take a look. If you want to get your hands dirty and submit a pull request, even better. Also, take a look at the test suite in `tests.py`
and tests your changes to make sure nothing else breaks. To run the tests, execute the following command:

	$ python tests.py

I really appreciate anything you can contribute to the library. 	

## License

[MIT Licence](https://github.com/svpino/rfeed/blob/master/LICENSE)

Copyright (c) 2014 Santiago Valdarrama

