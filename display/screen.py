#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Display manager
"""
# Python 2 and 3 compatibility
from __future__ import unicode_literals, print_function

import logging
import threading
import time
import Queue

from pphone.display.device import sh1106, const
from pphone.display.display import *
from pphone.display.pages import *



class ScreenManager(threading.Thread):
    _display_port = 1
    _display_address = 0x3C
    _instance = None
    _registry = None

    def __new__(cls, *args, **kwargs):
        # Singleton implementation
        if not cls._instance:
            cls._registry = Page
            cls._instance = super(ScreenManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self, queue, configuration={}):
        self.device = sh1106(port=self._display_port, address=self._display_address)
        self.config = configuration
        self.queue = queue
        # Just initialize the logger and enumerate the list of pages
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("List of Pages defined")
        for page_class_name in self._registry:
            page_class = self._registry[page_class_name]
            self.logger.debug("%s: %s" % (page_class_name, page_class.__name__))
            print(page_class, page_class_name)
        self.stoprequest = threading.Event()
        threading.Thread.__init__(self)


    def _page(self, page):
        page_instance = None
        page_name = page.page
        for page_class_name in self._registry:
            if page_class_name == page_name:
                try:
                    page_class = self._registry[page_name]
                    page_instance = page_class(self.device)
                    msg = "%s: %s" % (page_name, page_class.__name__)
                    self.logger.debug(msg)
                except Exception as e:
                    msg = "Cannot initialize '%s': %s" % (page_class_name, e)
                    self.logger.error(msg)
                    print(msg)
                    raise ValueError(msg)
                break
        else:
            msg = "Not found class Page to manage '%s'" % page_name
            self.logger.error(msg)
            raise LookupError(msg)
        return page_instance


    def join(self, timeout=None):
        self.stoprequest.set()
        super(ScreenManager, self).join(timeout)


    def run(self):
        page_instance = None
        data = None
        suspend = 0
        refresh = float(self.config["refresh"])
        if self.queue.empty():
            self.init()
        while not self.stoprequest.isSet():
            if not self.queue.empty():
                self.on()
                try:
                    try:
                        data = self.queue.get()
                    except Queue.Empty:
                        continue
                    try:
                        page_instance = self._page(data)
                    except ValueError:
                        self.logger.warn("Ignoring: %s" % data)
                    except LookupError:
                        self.logger.warn("Ignoring: %s" % data)
                    else:
                        self.logger.debug("Running: %s" % data)
                        if data.persistence > 0:
                            persistence = float(data.persistence)
                            refresh_counter = float(0)
                            while refresh_counter < persistence:
                                page_instance.run(data)
                                time.sleep(refresh)
                                refresh_counter += refresh
                        else:
                            page_instance.run(data)
                        suspend = 0
                    finally:
                        self.queue.task_done()
                except Exception as e:
                    print(e)
                    self.logger.error(e)
            else:
                try:
                    time.sleep(refresh)
                    if suspend <= self.config["suspend"]:
                        if suspend == int(self.config["suspend"]):
                            self.suspend()
                        else:
                            self.logger.debug("Re-Running: %s" % data)
                            page_instance.run(data)
                            suspend += 1
                except Exception as e:
                    print(e)
                    self.logger.error(e)


    def init(self, title="Hola Mundo!", text=[
        ("Initialization ... ", 'Hack-Regular.ttf', 12),
        (u"\uf253 \uf21e \uf1e4 \uf0c0", 'fontawesome-webfont.ttf', 18)]):
        
        self.device.command(
            const.SETCONTRAST, 0x7F,
            const.NORMALDISPLAY, 
            const.DISPLAYALLON_RESUME, 
            const.DISPLAYON
        )
        display = Display()
        display.title = title
        display.text = text
        display.persistence = 1
        self.queue.put(display)

    def on(self):
        self.logger.info("Power on display")
        self.device.command(const.DISPLAYALLON_RESUME, const.DISPLAYON)

    def off(self):
        self.queue.clear()
        self.logger.info("Power off display")
        self.device.command(const.DISPLAYOFF)

    def contrast(self, value=0xFF):
        self.logger.info("Setting contrast '%02x'" % value)
        self.device.command(const.SETCONTRAST, value)

    def suspend(self):
        self.logger.info("Suspending display")
        self.device.command(const.DISPLAYOFF)


