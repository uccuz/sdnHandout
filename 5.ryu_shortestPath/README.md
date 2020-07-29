# ryu shortestPath
實際建構shortestPath controller

## mininet延遲網路建置

#### import library
```shell=
from mininet.link import TCLink
```
#### 在連結下設定延遲
```shell=
net.addLink(s1, h1,cls=TCLink, delay="50ms")
```



## 測試

### 開啟ryu及mininet
```shell=
#開啟ryu controller
ryu-manager simpleSwitch.py
#開新視窗,啟動mininet
sudo mn --topo single,3 --mac --switch ovs,protocols=OpenFlow13 --controller=remote,ip=127.0.0.1
```
### ping
```shell=
h1 ping h2
h1 ping h3 
```

### 觀察封包
```shell=
s1 tcpdump
```

## 參考資料
[OpenFlow 實作的交換器](https://osrg.github.io/ryu-book/zh_tw/html/switching_hub.html)