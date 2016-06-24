#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Display manager
"""
# Python 2 and 3 compatibility
from __future__ import unicode_literals, print_function


import sys
import pjsua as pj


# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):
    def __init__(self, call=None):
        if call:
            self.call = weakref.proxy(call)
        else:
            self.call = None
        pj.CallCallback.__init__(self, call)


    def on_state(self):
        """Notification that the call's state has changed.
        """
        print "Call is ", self.call.info().state_text,
        print "last code =", self.call.info().last_code,
        print "(" + self.call.info().last_reason + ")"


    def on_media_state(self):
        """Notification that the call's media state has changed.
        """
        global lib
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            # Connect the call to sound device
            call_slot = self.call.info().conf_slot
            lib.conf_connect(call_slot, 0)
            lib.conf_connect(0, call_slot)
            print "Hello world, I can talk!"


    def on_dtmf_digit(self, digits):
        """Notification on incoming DTMF digits.
        Keyword argument:
        digits  -- string containing the received digits.
        """
        pass

    def on_transfer_request(self, dst, code):
        """Notification that call is being transferred by remote party.
        Application can decide to accept/reject transfer request by returning
        code greater than or equal to 500. The default behavior is to accept
        the transfer by returning 202.
        Keyword arguments:
        dst     -- string containing the destination URI
        code    -- the suggested status code to return to accept the request.
        Return:
        the callback should return 202 to accept the request, or 300-699 to
        reject the request.
        """
        return code

    def on_transfer_status(self, code, reason, final, cont):
        """
        Notification about the status of previous call transfer request.
        Keyword arguments:
        code    -- SIP status code to indicate completion status.
        text    -- SIP status reason phrase.
        final   -- if True then this is a final status and no further
                   notifications will be sent for this call transfer
                   status.
        cont    -- suggested return value.
        Return:
        If the callback returns false then no further notification will
        be sent for the transfer request for this call.
        """


