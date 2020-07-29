# -*- coding:utf-8 -*-
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink

if '__main__' == __name__:
	# 宣告 Mininet 使用的 Controller 種類
    net = Mininet(controller=RemoteController)
	
	# 指定 Controller 的 IP 及 Port，進行初始化
    c0 = net.addController('c0',ip='127.0.0.1', port=6633)
	
	# 加入 Switch
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
	
	# 加入主機，並指定 MAC，ip
    h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1')
    h2 = net.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.0.2')
	
	# 建立連線
    net.addLink(s1, h1)
    net.addLink(s5, h2)

    # 建立連線並設定延遲
    net.addLink(s1, s2,cls=TCLink, delay="10ms")
    net.addLink(s1, s3,cls=TCLink, delay="50ms")
    net.addLink(s2, s4,cls=TCLink, delay="20ms")
    net.addLink(s3, s5,cls=TCLink, delay="40ms")
    net.addLink(s4, s5,cls=TCLink, delay="30ms")


    # 建立 Mininet
    net.build()
	
    # 啟動 Controller
    c0.start()
	
    # 啟動 Switch，並指定連結的 Controller 為 c0
    s1.start([c0])
    s2.start([c0])
    s3.start([c0])
    s4.start([c0])
    s5.start([c0])



    # 執行互動介面(mininet>...)
    CLI(net)
	# 互動介面停止後，則結束 Mininet
    net.stop()