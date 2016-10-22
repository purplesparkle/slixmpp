"""
    Slixmpp: The Slick XMPP Library
    Copyright (C) 2011 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of Slixmpp.

    See the file LICENSE for copying permissio
"""

import logging

import slixmpp
from slixmpp.stanza import Message
from slixmpp.xmlstream.handler import Callback
from slixmpp.xmlstream.matcher import StanzaPath
from slixmpp.xmlstream import register_stanza_plugin, ElementBase, ET
from slixmpp.plugins import BasePlugin
from slixmpp.plugins.xep_0085 import stanza, ChatState


log = logging.getLogger(__name__)


class XEP_0085(BasePlugin):

    """
    XEP-0085 Chat State Notifications
    """

    name = 'xep_0085'
    description = 'XEP-0085: Chat State Notifications'
    dependencies = {'xep_0030'}
    stanza = stanza

    def plugin_init(self):
        self.xmpp.register_handler(
            Callback('Chat State',
                     StanzaPath('message/chat_state'),
                     self._handle_chat_state))

        register_stanza_plugin(Message, stanza.Active)
        register_stanza_plugin(Message, stanza.Composing)
        register_stanza_plugin(Message, stanza.Gone)
        register_stanza_plugin(Message, stanza.Inactive)
        register_stanza_plugin(Message, stanza.Paused)

    def plugin_end(self):
        self.xmpp.remove_handler('Chat State')

    def session_bind(self, jid):
        self.xmpp.plugin['xep_0030'].add_feature(ChatState.namespace)

    def _handle_chat_state(self, msg):
        state = msg['chat_state']
        log.debug("Chat State: %s, %s", state, msg['from'].jid)
        self.xmpp.event('chatstate', msg)
        self.xmpp.event('chatstate_%s' % state, msg)
