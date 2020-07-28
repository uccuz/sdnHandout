# -*- coding:utf-8 -*-
#create network and start command
from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet.node import RemoteController

tree4 = TreeTopo(depth=2,fanout=2)
net = Mininet(topo=tree4,controller=RemoteController)
net.start()
h1, h4  = net.hosts[0], net.hosts[3]
print h1.cmd('ping -c1 %s' % h4.IP())
net.stop()

# start command : sudo python topoWithStartCommand.py