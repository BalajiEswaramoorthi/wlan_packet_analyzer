import logging
from enum import IntEnum

class sta_state(IntEnum):
    PROBE = 1
    AUTH = 2
    ASSOC = 3
    KEY_EXCHANGE = 4
    CONNECTED = 5
    UNKNOWN = 6

class station():
    def __init__(self, mac):
        self.Mac = mac
        self.TxData = 0
        self.RxData = 0
        self.TxQosData = 0
        self.RxQosData = 0
        self.ap = None
        self.State = sta_state.UNKNOWN
        self.SessionStartTime = None
        self.SessionEndTime = None
        self.BlockAckSessions = []

    def UpdateAp(self, ap):
        self.ap = ap

    def total_session_time(self):
        return self.start_time - self.end_time

    def tx_data_packet(self):
        self.TxData += 1

    def rx_data_packet(self):
        self.RxData += 1

    def tx_qos_data(self):
        self.TxQosData += 1

    def rx_qos_data(self):
        self.RxQosData += 1

class AllStaList():
    def __init__(self):
        self.sta_count = 0
        self.sta_list = {}

    def add_sta(self, mac, sta):
        self.sta_list.update({mac:sta})
        self.sta_count += 1

    def FindSta(self, mac):
        return self.sta_list.get(mac)

    def remove_sta(self, sta_mac):
        del self.sta_list[sta_mac]
        self.sta_count -= 1

    def echoStats(self):
        logging.info("---------- PER STA STATS ----------")
        for mac, sta in self.sta_list.items():
            logging.info("MAC ADDRESS               : %s", mac)
            logging.info("TX DATA PACKETS           : %d", sta.TxData)
            logging.info("RX DATA PACKETS           : %d", sta.RxData)
            logging.info("TX QOS DATA               : %d", sta.TxQosData)
            logging.info("RX QOS DATA               : %d", sta.RxQosData)

g_sta_list = AllStaList()