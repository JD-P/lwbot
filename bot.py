from twisted.words.protocols import irc
from twisted.internet import protocol
import re
import plugins

def load_modules(plugins):
  dir(plugins)

class IrcBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        print msg
        if not user:
            return
        if self.username in msg:
            msg = re.compile(self.nickname + "[:,]* ?", re.I).sub('', msg)
            prefix = "%s: " % (user.split('!', 1)[0], )
            self.msg(self.factory.channel, prefix + ": this is a message")
        else:
            prefix = ''


class IrcBotFactory(protocol.ClientFactory):
    protocol = IrcBot

    def __init__(self, channel, nickname='LWBot'):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

from twisted.internet import reactor

plugins.modules["pomodoro"].pomo()




# if __name__ == "__main__":
#    load_modules()
#    chan = 'lw-pomodoro'  #sys.argv[1]
#    reactor.connectTCP('irc.freenode.net', 6667, IrcBotFactory('#' + chan))
#    reactor.run()
