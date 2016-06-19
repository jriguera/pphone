#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Display manager
"""
# Python 2 and 3 compatibility
from __future__ import unicode_literals, print_function

import sys
import os
import logging
import Queue
import time

# Append the current folder
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from pphone.display.screen import ScreenManager
from pphone.display.display import Display






symbols = [
    [(u'\uf0e8 ', 'fontawesome-webfont.ttf', 16), ("Connectivity", 'Hack-Regular.ttf', 12)],
    [(u'\uf0a2 ', 'fontawesome-webfont.ttf', 16), ("Bell enabled", 'Hack-Regular.ttf', 12)],
    [(u'\uf001 ', 'fontawesome-webfont.ttf', 16), ("Speakers", 'Hack-Regular.ttf', 12)],
    [(u'\uf095 ', 'fontawesome-webfont.ttf', 16), ("SIP phone", 'Hack-Regular.ttf', 12)],
    [(u'\uf110 ', 'fontawesome-webfont.ttf', 16), ("Dial available", 'Hack-Regular.ttf', 12)],
    [(u'\uf00c ', 'fontawesome-webfont.ttf', 16), ("Ready!", 'Hack-Regular.ttf', 12)],
]

def init(queue, symbols=[]):
    counter = 0
    show = symbols[0]
    for symbol in symbols:
        display = Display()
        display.title = "Starting" + "."*(counter % 4)
        display.text = symbol
        display.persistence = 1
        queue.put(display)
        counter += 1



def show_time():
    msg = time.strftime("%H:%M", time.localtime())
    font = ('Pixel_LCD-7.ttf', 22)
    pos = (24, 28)
    return (msg, font, pos)


def show_top_time():
    msg = time.strftime("%H:%M", time.localtime())
    font = ('Hack-Regular.ttf', 14)
    pos = (89, 0)
    return (msg, font, pos)


def show_top_status(internet=True, phone=True, call=True, bell=True, music=True):
    msg = u''
    if internet:
        msg += u'\uf0e8 '
    if call:
        msg += u'\uf2a0 '
    if music:
        msg += u'\uf001 '
    if bell:
        msg += u'\uf0a2 '
    if phone:
        msg += u'\uf095 '
    font = ('fontawesome-webfont.ttf', 14)
    pos = (0, 0)
    return (msg, font, pos)


def show_bottom_date():
    msg = time.strftime("%A, %d %B %Y", time.localtime())
    font = ('Cone.ttf', 12)
    pos = (0, 52)
    return (msg, font, pos)





displayqueue = Queue.Queue(10)
configuration = {
    "suspend": 600,
    "refresh": 0.5
}
displaythread = ScreenManager(displayqueue, configuration)
displaythread.setDaemon(True)
displaythread.start()



time.sleep(1)


init(displayqueue, symbols)

display = Display("desktop")
display.call = [
    {'fun': show_top_status, 'args':()},
    {'fun': show_top_time, 'args':()},
    {'fun': show_time, 'args':()},
    {'fun': show_bottom_date, 'args':()},
]
displayqueue.put(display)



#display = Display("phone")
#display.top = "S F G"
#display.msg = "RINGRING"
#display.bottom = "Adios"
#display.persistence = 5
#displayqueue.put(display)

#display = Display("control")
#display.cmd = 0xAE
#displayqueue.put(display)






time.sleep(10000)
