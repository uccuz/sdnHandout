# ryu LLDP
利用LLDP,取得topo資訊

參考： [SDN LAB3 — Ryu train( lldp )](https://medium.com/@kweisamx0322/sdn-lab3-ryu-train-f8fe13b03548)

## 拓樸圖

![](https://i.imgur.com/A230Cze.jpg)

## 測試

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