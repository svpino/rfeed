rfeed
=====

Python RSS 2.0 Generator

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
are sometimes hard to understand and isolated, so here is a full example from end to end:

```python
import datetime 
from rfeed import *

item1 = Item(
	title = "First article",
	link = "http://www.example.com/articles/1", 
	description = "This is the description of the first article",
    author = "Santiago L. Valdarrama",
    guid = Guid("http://www.example.com/articles/1"),
	pubDate = datetime.datetime.now())

item2 = Item(
	title = "Second article",
	link = "http://www.example.com/articles/2", 
	description = "This is the description of the second article",
    author = "Santiago L. Valdarrama",
    guid = Guid("http://www.example.com/articles/2"),
	pubDate = datetime.datetime.now())

feed = Feed(
	title = "Sample RSS Feed",
	link = "http://www.example.com/rss"
	description = "This is an example of how to use rfeed to generate an RSS 2.0 feed",
	language = "en-US",
	lastBuildDate = datetime.datetime.now(),
	items = [item1, item2])

print feed.rss()	

```

## Inspiration

I created my own [blog](https://blog.svpino.com) engine in Python for [Google App Engine](https://cloud.google.com/appengine/), 
thus I needed a way to generate my RSS feed. Later on, I added a [podcast](https://en3y2.svpino.com) site that also needed an RSS 
feed, but this time with [iTunes](https://www.apple.com/itunes/podcasts/specs.html) support.

The only help I could find was the amazing [PyRSS2Gen](http://www.dalkescientific.com/Python/PyRSS2Gen.html) library written by 
Andrew Dalke. The library is very simple, but it didn't help with the iTunes support, so I found myself modifying it to get as 
much as I could out of it.

At the end I didn't like what I did to the original library: it was messy all around. It wasn't the library's fault, but my 
own. I decided to fix the problem from scratch, by rewriting the library in a different way.

I'm not claming this new version is better than the original. It's just different and I think a little bit easier to extend and 
maintain (since it comes with a full suite full of unit tests). Since I needed iTunes support from the beginning, I also coded an 
iTunes extension for the library. Now I'm powering my blog and podcast with it, and I hope it serves well to anyone with similar needs.

Thanks to Andrew Dalke for writing the first version a long time ago. This project is based on his original work, borrowing ideas
and code from it.

## Contributing

Contributions, questions and comments are all welcome and encouraged.

### Running the unit tests

To run the tests, execute the following command:

	$ python tests.py

## License

MIT Licence

Copyright (c) 2014 Santiago Valdarrama

