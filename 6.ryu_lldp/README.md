# ryu LLDP
利用LLDP,取得topo資訊

參考： [SDN LAB3 — Ryu train( lldp )](https://medium.com/@kweisamx0322/sdn-lab3-ryu-train-f8fe13b03548)

## 拓樸圖

![](https://i.imgur.com/A230Cze.jpg)

## 技術

## 測試

### switch一開始連上controller的設定
```python=
@set_ev_cls(ofp_event.EventOFPSwitchFeatures,CONFIG_DISPATCHER)
def switch_features_handler(self, ev):
    #當封包為LLDP時，傳送給controller
    match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_LLDP
    self.send_port_desc_stats_request(datapath)# send the request
```

### 開啟ryu及mininet
```shell=
#開啟ryu controller
ryu-manager ryuSpanningTree.py
#開新視窗,啟動mininet
sudo python topoSpanningTree.py
```
- 觀察是否由讀取到線路資訊

## 參考資料

[SDN LAB3 — Ryu train( lldp )](https://medium.com/@kweisamx0322/sdn-lab3-ryu-train-f8fe13b03548)

[資訊人筆記Lab3](https://www.kshuang.xyz/doku.php/ccis_lab:sdn:hw3)