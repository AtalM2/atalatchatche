#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run this script with one argument, the channel :

    $ ./bot.py ##atal
"""

from bicloo import bicloo
from fortune_teller import fortune_teller
from ics import ics
import re
import sys
from twisted.internet import protocol
from twisted.internet import reactor
from twisted.words.protocols import irc


def splitUserString(user_string):
    """
    Splits a full user string to return only the user name.
    For example, m0g!~Mog@88.191.117.112 → m0g
    """
    return user_string.split('!', 1)[0]


class Atalatchatche(irc.IRCClient):
    """ATAL's irc bot"""

    pattern = re.compile(u'^# *')
    nickname = 'atalatchatche'

    def __init__(self, channel):
        self.channel = channel

    # callbacks for events
    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.msg(channel,
                 '♥ Salut {channel} ♥'.format(channel=self.factory.channel))

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = splitUserString(user)

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            pass
        # Otherwise check to see if it's a command
        elif channel == self.channel and msg.startswith('#'):
            command = self.pattern.sub('', msg, 1).rstrip()
            print 'received command ' + command
            split = map(lambda x: x.strip(), command.split(' ', 2))
            if not split:
                return
            else:
                function = split[0]
                if function in ['help', 'h4lp']:
                    self.msg(self.channel,
                             ("Je comprends les commandes:\n"
                              "- bow :            je fais la carpette\n"
                              "- bicloo station : je donne des infos "
                              "sur la station donnée en arg "
                              "(lowercase et sans accent). Liste des "
                              "stations dispo ici : "
                              "http://www.bicloo.nantesmetropole.fr"
                              "/Les-stations/Plan-des-stations-en-PDF"
                              "/Consultez-le-plan\n"
                              "- cours :          je donne des infos "
                              "sur le prochain cours qui aura lieu\n"
                              "- shine :          je vous éblouis "
                              "en racontant des trucs super "
                              "intéressants"))
                elif function == 'bow':
                    self.describe(self.channel, "s'incline")
                elif function == 'bicloo':
                    if len(split) < 2:
                        self.msg(self.channel,
                                 "j'ai besoin d'un nom de station ;(")
                        return
                    station = split[1]
                    self.msg(self.channel, bicloo(station))
                elif function == 'cours':
                    self.msg(self.channel, ics())
                elif function == 'shine':
                    self.msg(self.channel, fortune_teller())

    # irc callbacks
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '`'


class BotFactory(protocol.ClientFactory):
    """
    A factory for bots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        p = Atalatchatche(self.channel)
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed: ", reason
        reactor.stop()


if __name__ == '__main__':
    # create factory protocol and application
    f = BotFactory(sys.argv[1])

    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()














