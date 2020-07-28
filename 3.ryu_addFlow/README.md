# ryu add flow

利用RYU下達flow使Host用不同方式接通
- 方式
    1. port轉發
    2. mac轉發
    3. ip轉發

- 路徑: h1 -> s1 -> s2 -> h2

## 拓樸圖

![](https://i.imgur.com/A230Cze.jpg)
- 使用mininet建置

## 實作

### port轉發條件
```python=
match = parser.OFPMatch(in_port=1)
```
- 輸入port為1

### mac轉發條件
```shell=
match = parser.OFPMatch(in_port=1,eth_src='00:00:00:00:00:01')
```
- 輸入port為1,eth_src='00:00:00:00:00:01'

### ip轉發條件
ping時會先發起arp找到mac，之後才會使用ip請求，所以兩者皆須設定
```shell=
#設定arp轉發
match = parser.OFPMatch(in_port=1,eth_type=0x806)
```
- 輸入port為1,且為arp request
```shell=
#設定ip轉發
match = parser.OFPMatch(in_port=1,eth_type=0x800,ipv4_src='10.0.0.1')
```
- 輸入port為1,且為ip request,ipv4_src='10.0.0.1'

### 轉發方式
```shell=
actions = [parser.OFPActionOutput(port=2)]
self.add_flow(datapath, 0 ,match,actions)
```
- 當符合條件，將封包送至port2

### 指定特定switch
```shell=
ev.msg.datapath.id == 1:
```
- 添加在switch 1上



## 測試

### 開啟ryu及mininet
```shell=
#開啟ryu controller
ryu-manager ryuAddFlow.py
#開新視窗,啟動mininet
sudo python topoAddFlow.py
```
### 檢查flow
```shell=
sh ovs-ofctl dump-flows s1
sh ovs-ofctl dump-flows s2
```
### ping
```shell=
#相通
h1 ping h2 -c 2
不相通
h1 ping h3 -c 2
```



## 參考資料
[Ping fails in Mininet, RYU - OpenFlow 1.3](https://stackoverflow.com/questions/36197923/ping-fails-in-mininet-ryu-openflow-1-3)

[OpenFlow & Mininet](http://www.cs.nchu.edu.tw/~snmlab/CloudMgnt201409/Lab3.html)