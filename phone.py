#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Display manager
"""
# Python 2 and 3 compatibility
from __future__ import unicode_literals, print_function

import pjsua

class Simplecall:
    def __init__(self):
        self.pj = pjsua.Lib()
        self.pj.init()
        self._pj_start()
        self.call = None

    def _pj_reload(self):
        self._pj_stop()
        self.pj = pjsua.Lib()
        self.pj.init()
        self._pj_start()

    def _pj_start(self):
        try:
            self.transport = self.pj.create_transport(pjsua.TransportType.UDP, pjsua.TransportConfig(5070))
            self.pj.set_snd_dev(self.settings.config['capture'], self.settings.config['output'])
            self.pj.start()
            self.acc = self.pj.create_account(pjsua.AccountConfig(self.settings.config['server'], self.settings.config['login'], self.settings.config['password']))
            acc_cb = AccountCallback(self.acc)
            acc_cb.connect('register', self.register)
            acc_cb.connect('incoming', self.incoming)
            self.acc.set_callback(acc_cb)
        except:
            pass

    def _pj_stop(self):
        try:
            self.pj.hangup_all()
            if self.acc is not None:
                self.acc.delete()
            if self.pj:
                self.pj.destroy()
            self.pj = None
        except:
            pass


#################################


    def _load_settings(self):
        self.config = _decode_dict(json.load(open('config.json')))

        self.server.set_text(self.config['server'])
        self.port.set_text(self.config['port'])
        self.login.set_text(self.config['login'])
        self.password.set_text(self.config['password'])
        self.capture.set_active(self.config['capture'])
        self.output.set_active(self.config['output'])

    def save_settings(self):
        self.config.update({'server': self.server.get_text(), 'port': self.port.get_text(),
                            'login': self.login.get_text(), 'password': self.password.get_text(),
                            'capture': self.capture.get_active(), 'output': self.output.get_active()})
        json.dump(self.config, open('config.json', 'w'))
        self.hide()


###############################




    def incoming(self, widget, call):
        if self.call:
            call.answer(code=486)
            return
        self.call= call
        call_cb = CallCallback(self.call)
        call_cb.connect('state', self.on_state)
        self.call.set_callback(call_cb)
        self.switch_stack('incoming', self.call.info().uri)


    def make_call(self, widget):
        self.call = self.acc.make_call('sip:{0}@{1}'.format(self.number_entry.get_text(), self.settings.config['server']))
        call_cb = CallCallback(self.call)
        call_cb.connect('state', self.on_state)
        self.call.set_callback(call_cb)
        self.switch_stack('call', 'Calling {0}'.format(self.number_entry.get_text()))


    def hungup_call(self, widget):
        self.call.hangup()

    def answer_call(self, widget):
        self.call.answer()


    def on_state(self, widget, state):
        if state == pjsua.CallState.DISCONNECTED:
            self.switch_stack('dialer')
            self.call = None
        elif state == pjsua.CallState.CONNECTING:
            self.switch_stack('call', self.call.info().uri)
        elif state == pjsua.CallState.CONFIRMED:
            self.switch_stack('call', self.call.info().uri)


if __name__ == "__main__":
    sc = Simplecall()

