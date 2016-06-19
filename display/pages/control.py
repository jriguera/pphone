#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Special page to control the device
"""
# Python 2 and 3 compatibility
from __future__ import unicode_literals, print_function

from pphone.display.display import Page



class Control(Page):
    name = "control"

    def show(self, display):
        if self.done == 0:
            self.logger.debug("Sending control data: %s" % display)
            if isinstance(display.cmd, (int, long, float, complex)):
                self.device.command(display.cmd)
            else:
                for cmd in display.cmd:
                    self.device.command(cmd)

