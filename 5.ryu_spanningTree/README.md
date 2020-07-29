# ryu spanning tree
實作spanning tree,防止網路拓樸出現迴圈

參考： [生成樹（ Spanning Tree ）](https://osrg.github.io/ryu-book/zh_tw/html/spanning_tree.html)

## 拓樸圖

![](https://i.imgur.com/eHvQErQ.png)

## 測試

### 開啟ryu及mininet
```shell=
#開啟ryu controller
ryu-manager ryuSpanningTree.py
#開新視窗,啟動mininet
sudo python topoSpanningTree.py
```
### ping
```shell=
pingall 
```

### 觀察各switch的規則
```shell=
sh ovs-ofctl dump-flows s1
sh ovs-ofctl dump-flows s2
sh ovs-ofctl dump-flows s3
```


## 參考資料
參考： [生成樹（ Spanning Tree ）](https://osrg.github.io/ryu-book/zh_tw/html/spanning_tree.html)