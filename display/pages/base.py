#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Initial desktop
"""
# Python 2 and 3 compatibility
from __future__ import unicode_literals, print_function

import os.path

from PIL import ImageFont

from pphone.display.display import Page



class Base(Page):
    name = "base"
    spacing = 6

    def show(self, display):
        with self.canvas as draw:
            size = (0, 0)
            pos = (0, 0)
            if display.title:
                draw.text((0, 0), display.title, font=self.font, fill=255)
                size = self.font.getsize(display.title)
                pos = (0, self.spacing + size[1])
            # [(text, font, size), ]
            for (text, f, fsize) in display.text:
                if f:
                    font_path = os.path.join(self.folder, 'fonts', f)
                    font = ImageFont.truetype(font_path, fsize)
                else:
                    font = self.font
                draw.text(pos, text, font=font, fill=255)
                size = font.getsize(text)
                pos = (pos[0] + size[0], pos[1])
                if pos[0] >= self.device.width:
                    pos = (0, pos[1] + self.spacing + size[1])
                    






#    def show(self, display):
#        font_path = os.path.join(self.folder, self.font_symbol)
#        font = ImageFont.truetype(font_path, self.font_symbol_size)
#        with self.canvas as draw:
#            draw.text((0, 0), display.symbol, font=font, fill=255)
#            draw.text((0, 20), display.msg, font=self.font, fill=255)
#            draw.text((0, 50), display.bottom, font=self.font, fill=255)

