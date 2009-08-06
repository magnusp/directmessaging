from morbid import StompFactory

from twisted.protocols import basic
from twisted.internet import reactor, protocol
from twisted.internet.task import LoopingCall
from stompservice import StompClientFactory
import simplejson as json

class MyReceiver(basic.LineReceiver):
    delimiter = '\0'
    def connectionMade(self):
        print "Got new client!"
        self.factory.clients.append(self)
    def connectionLost(self, reason):
        print "Lost a client!"
        self.factory.clients.remove(self)
    def lineReceived(self,line):
        if line == "<policy-file-request/>":
            print "\t sending policy file"
            self.sendLine("<?xml version=\"1.0\"?><cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"61613\" /></cross-domain-policy>")
        else:
            print line

class XMLSocket(protocol.Factory):
    clients=[]
    def __init__(self, protocol=None):
        self.protocol=protocol

'''
	The DataProducer is an example of how you can hook into the
	broker. Here, we send a simple text string every second given
	that shouldSend is true.
'''
class DataProducer(StompClientFactory):
    shouldSend = True
    def recv_connected(self, msg):
        self.timer = LoopingCall(self.send_data)
        self.timer.start(1000/1000.0)
 
    def send_data(self):
        if self.shouldSend:
            self.send("/topic/directmessaging-outgoing", "Hello world")

def main():
    # The STOMP broker
    reactor.listenTCP(61613, StompFactory()) 

    # Flash socket policy serving
    reactor.listenTCP(33333, XMLSocket(MyReceiver)) 

    # And the example DataProducer
    dp = DataProducer()
    dp.shouldSend = False
    reactor.connectTCP('localhost', 61613, dp)

    # Start everything
    reactor.run()

if __name__ == "__main__":
    main()