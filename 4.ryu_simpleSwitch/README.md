# ryu simple switch
實際了解simple switch運作原理,詳見code

參考： [OpenFlow 實作的交換器](https://osrg.github.io/ryu-book/zh_tw/html/switching_hub.html)

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