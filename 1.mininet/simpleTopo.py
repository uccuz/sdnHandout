# -*- coding:utf-8 -*-
#建立簡單拓樸
#Topo : host --- switch --- switch --- host
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController

if '__main__' == __name__:
    # 宣告 Mininet 使用的 Controller 種類
    net = Mininet(controller=RemoteController)

    # Add hosts and switches
    leftHost = net.addHost('h1')
    rightHost = net.addHost('h2')
    leftSwitch = net.addSwitch('s3')
    rightSwitch = net.addSwitch('s4') 
    # Add links
    net.addLink(leftHost , leftSwitch)
    net.addLink(leftSwitch , rightSwitch)
    net.addLink(rightSwitch , rightHost) 
    
    net.start()
    # 執行互動介面(mininet>...)
    CLI(net)
	# 互動介面停止後，則結束 Mininet
    net.stop()
        
# start command : sudo python simpleTopo.py