# mininet
介紹如何使用mininet建立拓樸和mininet常用指令

## 安裝
```shell=
git clone git://github.com/mininet/mininet 
mininet/util/install.sh -a
```

## 建立topo

### 使用預設topo
```shell=
sudo mn
#若上次沒清乾淨
sudo mn -c
```
### delay參數
```shell=
sudo mn --link tc,bw=10,delay=10ms
```
### 建立線性topo
```shell=
sudo mn --topo=linear,3
```
### 建立樹狀topo
```shell=
sudo mn --topo tree,depth=2,fanout=8
```
### Controller設定
```shell=
sudo mn --mac --switch ovs,protocols=OpenFlow13 --controller=remote,ip=127.0.0.1
```
- --mac : mac 使用內建的方式編排
- --switch ovs : 使用OpenVSwitch
- --protocols=OpenFlow13 : 選擇 Openflow 的版本，預設為1.0
- --controller=remote : 使用外部的 controller 來控制 Mininet

### 使用已寫好topo
```shell=
sudo python <fileName>
```

## CLI指令

### 幫助
```shell=
help
```
### Display nodes
```shell=
nodes
```
### Display links
```shell=
net
```
### Dump information about all nodes
```shell=
dump
```
### Run a command on a host process
```shell=
h1 ifconfig -a
h1 ping -c 3 h2
```
### 對全部ping
```shell=
pingall
```
### 開啟獨立視窗
```shell=
xterm h1
```
### 清除與新增網路設定
```shell=
xterm h1
#清除設定
ifconfig h1-eth0 0
#新增設定
ip addr add 192.168.1.1/24 brd + dev h1-eth0
```
### 開啟關閉連結
```shell=
#關閉
link h2 s1 down
#開啟
link h2 s1 up
```

### 測試節點之間效能
```shell=
iperf h1 h2
```

### 建立http server
```shell=
#開啟http server
h2 python -m SimpleHTTPServer 80 &
#測試http server的反應
h1 wget -O - h2
#關閉http server
h2 kill %python
```
### 擷取封包
```shell=
#擷取s1封包
s1 tcpdump
```

### 查看 Open vSwitch 的狀態
```shell=
#查詢OVS的bridge
sh ovs-vsctl show
#管理OVS的datapath
sh ovs-dpctl show
```

### flow設定

#### 查看flow
```shell=
#看s1
sh ovs-ofctl dump-flows s1
```
#### 新增flow
```shell=
#新增s1
sh ovs-ofctl add-flow s1 "priority=0,action=normal"
```
- action=normal:讓封包能正常傳遞

#### 刪除flow
```shell=
#刪除s1
sh ovs-ofctl del-flows s1
```

## 參考資料
[Mininet Installation](https://myweb.ntut.edu.tw/~phtseng/SDN/LAB1.pdf)

[Learn Mininet](https://github.com/YanHaoChen/Learning-SDN/tree/master/Mininet)