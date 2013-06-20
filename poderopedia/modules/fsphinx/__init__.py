#!/usr/bin/env python

"""fSphinx easily builds faceted search systems using Sphinx."""

__version__ = '0.5'
__author__ = 'Alex Ksikes <alex.ksikes@gmail.com>'
__license__ = 'LGPL'


from fsphinx.facets import *
from hits import *
from queries import *
from fsphinx.sphinx import FSphinxClient
from fsphinx.cache import RedisCache
from pretty_url import *
from fsphinx.utils import *