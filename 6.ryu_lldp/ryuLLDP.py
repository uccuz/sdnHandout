# -*- coding:utf-8 -*-
# 程式碼參考: https://medium.com/@kweisamx0322/sdn-lab3-ryu-train-f8fe13b03548

from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3
from ryu.controller.handler import set_ev_cls
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.lib.packet import ether_types,lldp,packet,ethernet


class MySwitch(app_manager.RyuApp):
    #使用 openflow1.3
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    #儲存連結
    link = []

    def __init__(self, *args,**kwargs):
        super(MySwitch,self).__init__(*args,**kwargs)
        #定義 mac 位址表
        self.mac_to_port = {}
    #Event handler,一開始連上controller的設定(SwitchFeatures)
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures,CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        #用來處理 OpenFlow 交換器重要訊息
        datapath = ev.msg.datapath
        #表示對應的 ofproto module
        ofproto = datapath.ofproto
        #表示對應的 ofproto_parser module
        parser = datapath.ofproto_parser

        #當封包為LLDP時，傳送給controller
        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_LLDP)
        
        #Controller 指定為封包的目的地,OFPCML_NO_BUFFER 設定為 max_len
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]

        #發送 Flow Mod 訊息
        self.add_flow(datapath, 1, match, actions)
        
        #送一個port資訊要求給各個switch
        self.send_port_desc_stats_request(datapath)


    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        #表示對應的 ofproto module
        ofproto = datapath.ofproto
        #表示對應的 ofproto_parser module
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)


    def send_port_desc_stats_request(self, datapath):
        #表示對應的 ofproto module
        ofproto = datapath.ofproto
        #表示對應的 ofproto_parser module
        ofp_parser = datapath.ofproto_parser
    
        #來取得 switch port 的 mac address
        req = ofp_parser.OFPPortDescStatsRequest(datapath, 0)
        datapath.send_msg(req)


    #發送 lldp 封包
    def send_lldp_packet(self, datapath, port, hw_addr, ttl):
        #表示對應的 ofproto module
        ofproto = datapath.ofproto
        #表示對應的 ofproto_parser module
        ofp_parser = datapath.ofproto_parser

        #產生一個封包object
        pkt = packet.Packet()
        #ethertype: LLDP
        #src: 發送 LLDP 的 switch port 的 mac
        #dst: LLDP_MAC_NEAREST_BRIDGE
        pkt.add_protocol(ethernet.ethernet(ethertype=ether_types.ETH_TYPE_LLDP,src=hw_addr ,dst=lldp.LLDP_MAC_NEAREST_BRIDGE))

        #chassis_id: 發送 LLDP 封包的 switch id
        chassis_id = lldp.ChassisID(subtype=lldp.ChassisID.SUB_LOCALLY_ASSIGNED, chassis_id=str(datapath.id))
        #port_id: 發送 LLDP 封包的 switch port id
        port_id = lldp.PortID(subtype=lldp.PortID.SUB_LOCALLY_ASSIGNED, port_id=str(port))

        #Time to live 
        ttl = lldp.TTL(ttl=10)
        end = lldp.End()
        tlvs = (chassis_id,port_id,ttl,end)
        pkt.add_protocol(lldp.lldp(tlvs))
        pkt.serialize()

        #self.logger.info("packet-out %s" % pkt)

        data = pkt.data
        actions = [ofp_parser.OFPActionOutput(port=port)]
        out = ofp_parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=ofproto.OFPP_CONTROLLER,
                                  actions=actions,
                                  data=data)
        datapath.send_msg(out)

    #請求的回應
    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply, MAIN_DISPATCHER)
    def port_desc_stats_reply_handler(self, ev):
        #用來處理 OpenFlow 交換器重要訊息
        datapath = ev.msg.datapath
        #表示對應的 ofproto module
        ofproto = datapath.ofproto
        #表示對應的 ofproto_parser module
        ofp_parser = datapath.ofproto_parser
        ports = []
        
        for stat in ev.msg.body:
            if stat.port_no <=ofproto.OFPP_MAX: 
                ports.append({'port_no':stat.port_no,'hw_addr':stat.hw_addr})
        for no in ports:
            in_port = no['port_no']
            match = ofp_parser.OFPMatch(in_port = in_port)
            for other_no in ports:
                if other_no['port_no'] != in_port:
                    out_port = other_no['port_no']
            self.send_lldp_packet(datapath,no['port_no'],no['hw_addr'],10)
            actions = [ofp_parser.OFPActionOutput(out_port)]
            self.add_flow(datapath, 1, match, actions)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser


        pkt = packet.Packet(data=msg.data)
        dpid = datapath.id # switch id which send the packetin
        in_port  = msg.match['in_port']

        pkt_ethernet = pkt.get_protocol(ethernet.ethernet)
        pkt_lldp = pkt.get_protocol(lldp.lldp)
        if not pkt_ethernet:
            return 
        #print(pkt_lldp)
        if pkt_lldp:
            self.handle_lldp(dpid,in_port,pkt_lldp.tlvs[0].chassis_id,pkt_lldp.tlvs[1].port_id)


        #self.logger.info("packet-in %s" % (pkt,))

    # Link two switch
    def switch_link(self,s_a,s_b):
        return s_a + '<--->' + s_b
            
    def handle_lldp(self,dpid,in_port,lldp_dpid,lldp_in_port):
        switch_a = 'switch'+str(dpid)+', port'+str(in_port)
        switch_b = 'switch'+lldp_dpid+', port'+lldp_in_port
        link = self.switch_link(switch_a,switch_b)

        # Check the switch link is existed
        if not any(self.switch_link(switch_b,switch_a) == search for search in self.link):
            self.link.append(link)


        print(self.link)
