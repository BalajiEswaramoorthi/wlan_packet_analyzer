import logging
from wlan import *
from AccessPoint import *
from station import *

_gDataStats = 0

__all__ = [ "dataFrame" ]

class _DataSubtype(IntEnum):
    Data = 0
    QosData = 8
    QosNull = 12

class dataFrame():
    def __init__(self) -> None:
        self.data = 0
        self.qos_data = 0
        self.qos_null = 0

    def echoStats(self):
        logging.info("DATA                  = %d", self.data)
        logging.info("QOS_DATA              = %d", self.qos_data)
        logging.info("QOS_NULL              = %d", self.qos_null)

    def process_data_frames(self, frame):
        mac = wlan_field(frame, "wlan.ta")
        sta = g_sta_list.FindSta(mac)
        if (not sta):
            ap = g_ap_list.FindAcessPoint(mac)
            if (not ap):
                logging.warning("data frame %s received before STA or AP add", mac)
                return
            ap.info.TxData += 1
        else:
            sta.tx_data_packet()
            mac = wlan_field(frame, "wlan.ra")
            ap = g_ap_list.FindAcessPoint(mac)
            if (ap):
                ap.info.RxData += 1
        self.data += 1

    def process_qos_data_frames(self, frame):
        mac = wlan_field(frame, "wlan.ta")
        sta = g_sta_list.FindSta(mac)
        if (not sta):
            ap = g_ap_list.FindAcessPoint(mac)
            if (not ap):
                logging.warning("data frame %s received before AP add", mac)
                return
            ap.QosDataTx()
        else:
            sta.tx_qos_data()
            mac = wlan_field(frame, "wlan.ra")
            ap = g_ap_list.FindAcessPoint(mac)
            ap.QosDataRx()
        self.qos_data += 1

    def process_qos_null(self, frame):
        self.qos_null += 1

    def data_frame(self, frame):
        sub_type = int(wlan_field(frame, "wlan.fc.subtype"))
        match sub_type:
            case _DataSubtype.Data:
                self.process_data_frames(frame)
            case _DataSubtype.QosData:
                self.process_qos_data_frames(frame)
            case _DataSubtype.QosNull:
                self.process_qos_null(frame)