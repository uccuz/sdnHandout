# ryu shortestPath
實際建構shortestPath controller

## 拓樸圖

![](https://i.imgur.com/kF7VHe5.png)

## mininet延遲網路建置

#### import library
```shell=
from mininet.link import TCLink
```
#### 在連結下設定延遲
```shell=
net.addLink(s1, h1,cls=TCLink, delay="50ms")
```

## 參考資料

[SDN LAB3 — Ryu train( lldp )](https://medium.com/@kweisamx0322/sdn-lab3-ryu-train-f8fe13b03548)

[基于跳数\时延\带宽的最短/优路径和负载均衡](http://www.muzixing.com/pages/2016/07/08/ji-yu-tiao-shu-shi-yan-dai-kuan-de-zui-duan-you-lu-jing-he-fu-zai-jun-heng.html)