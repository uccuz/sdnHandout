# ryu start up
介紹如何啟用ryu,連接mininet,以及使用REST API新增rule

參考： [RYU Controller with
Mininet](https://myweb.ntut.edu.tw/~phtseng/SDN/LAB2.pdf)

## 安裝
```shell=
sudo git clone git://github.com/osrg/ryu.git
sudo cd ryu
sudo python ./setup.py install
```

## 使用內建ryu controller連接

### 開啟Ryu controller
```shell=
- ryu-manager ryu.app.simple_switch_13
```
- simple_switch_13能實驗簡單交換器的功能

    - 分派網路內封包的流向
    - 處理不明封包

### 執行mininet
```shell=
sudo mn --topo=linear,3 --mac --controller=remote
```
- pingall試試看cintroller能否順利運作

### Ryu的圖形化介面
```shell=
#重新啟動ryu
ryu-manager ryu.app.simple_switch_13 ryu.app.gui_topology.gui_topology
```
- 127.0.0.1:8080，可看到連接方式

## 利用REST API 對controller下Flow(postman)

### 開啟Ryu(須掛載REST API)
```shell=
ryu-manager --verbose --observe-links ryu.app.ofctl_rest
```
### 建立topo
```shell=
sudo mn --mac --controller=remote,ip=127.0.0.1
```
- 此時ping結果不通，因為沒有任何規則

### REST API

#### 取得所有連接到controller的Switch
- HTTP Method : GET
```shell=
http://127.0.0.1:8080/stats/switches
```
### 取得指定Switch中的Flow
- HTTP Method : GET
```shell=
#取得switch1的flow
http://127.0.0.1:8080/stats/flow/1
```
### 新增一條Flow
- HTTP Method : POST
```shell=
#取得switch1的flow
http://127.0.0.1:8080/stats/flowentry/add
```
- Post內容(Body->raw輸入)
```json=
{
    "dpid": 1,
    "match":{
        "in_port":1
    },
    "instructions": [
        {
            "type": "APPLY_ACTIONS",
            "actions": [
                {
                    "type": "OUTPUT",
                    "port": 2
                }
            ]
        }
    ]
}
```
- 另外一邊也要輸入(1->2,2->1)

### 刪除指定Switch裡的所有Flow
- HTTP Method : DELETE
```shell=
#刪除switch1的flow
http://127.0.0.1:8080/stats/flowentry/clear/1
```

### 重啟topo
- 檢查flow
```shell=
- 檢查switch1的flow
sh ovs-ofctl dump-flows s1
```
- 試著pingall看看

## 參考資料
[RYU Controller with
Mininet](https://myweb.ntut.edu.tw/~phtseng/SDN/LAB2.pdf)