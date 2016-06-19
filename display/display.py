#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Display manager
"""
# Python 2 and 3 compatibility
from __future__ import unicode_literals

import os.path
import logging

from PIL import Image, ImageDraw, ImageFont



class Canvas(object):
    """
    A canvas returns a properly-sized `ImageDraw` object onto which the caller
    can draw upon. As soon as the with-block completes, the resultant image is
    flushed onto the device.
    """
    def __init__(self, device):
        self.draw = None
        self.image = Image.new('1', (device.width, device.height))
        self.device = device

    def __enter__(self):
        #self.image = Image.new('1', (self.device.width, self.device.height))
        self.draw = ImageDraw.Draw(self.image)
        return self.draw

    def __exit__(self, type, value, traceback):
        if type is None:
            # do the drawing onto the device
            self.device.display(self.image)
        del self.draw
        #del self.image
        return False



class MetaPage(type):
    """
    Metaclass to register automatically all the Pages
    """

    # using __init__ rather than __new__ here because I want to modify 
    # attributes of the class *after* they have been created
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'registry'):
            # this is the base class.  Create an empty registry
            cls.registry = {}
        else:
            # this is a derived class.  Add cls to the registry
            # if the class has the protocol attribute
            try:
                cls.registry[cls.name] = cls
            except:
                pass
        super(MetaPage, cls).__init__(name, bases, dct)

    # Metamethods, called on class objects:
    def __getitem__(cls, key):
        return cls.registry[key]

    def __iter__(cls):
        return iter(cls.registry)



class Display(object):
    """
    Transfer Object with information of each page
    """

    def __init__(self, page="base"):
        data = {
            "title": None,
            "text": [],
        }
        super(Display, self).__setattr__('data', data)
        super(Display, self).__setattr__('page', page)
        super(Display, self).__setattr__('persistence', float(0))

    def __getattr__(self, key):
        # The real attributes use __getattribute__
        try:
            return self.data[key]
        except:
            return None

    def __setattr__(self, key, value):
        if key == 'page':
            super(Display, self).__setattr__('page', value)
        elif key == 'persistence':
            super(Display, self).__setattr__('persistence', float(value))
        else:
            self.data[key] = value

    def __contains__(self, key):
        return key in self.data

    def __repr__(self):
        name = self.__class__.__name__
        page = self.page
        persistence = self.persistence
        data = str(self.data)
        show = "<%s:%s:%s %s>" % (name, page, persistence, data)
        return show

    def __str__(self):
        return str(self.data)



class Page(object):
    """
    Base class for all screen pages (see pages implementation in pages folder)
    """
    __metaclass__ = MetaPage
    font_name = 'Commodore_Angled_v1.2.ttf'
    font_size = 14

    def __init__(self, device):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.folder = os.path.abspath(os.path.dirname(__file__))
        font = os.path.join(self.folder, 'fonts', self.font_name)
        self.font = ImageFont.truetype(font, self.font_size)
        self.canvas = Canvas(device)
        self.device = device
        self.done = 0

    def __str__(self):
        show = "<%s: [%s]>" % (self.__class__.__name__, self.canvas)
        return show

    def run(self, display):
        self.logger.debug("Show: %s" % display)
        self.show(display)
        self.done += 1

    def show(self, data):
        pass


