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



class Desktop(Page):
    name = "desktop"

    def __init__(self, device):
        super(Desktop, self).__init__(device)
        self.clean = []

    def show(self, display):
        self.logger.debug("Desktop: %s" % display)
        with self.canvas as draw:
            # Clean the previous text positions
            for (xy, s) in self.clean:
                draw.line([xy[0], xy[1], xy[0]+s[0], xy[1]+s[1]], width=s[0], fill=0)
            self.clean = []
            for cmd in display.call:
                command = cmd['fun']
                msg, font, pos = command(*cmd['args'])
                if font:
                    font_path, font_size = font
                    font_path = os.path.join(self.folder, 'fonts', font_path)
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = self.font
                draw.text(pos, msg, font=font, fill=255)
                self.clean.append((pos, font.getsize(msg)))
                font = None

