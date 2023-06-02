import logging
from dataclasses import dataclass

@dataclass
class APinfo():
    MAC : str
    Capablity : int = 0
    BeaconSent : int = 0
    RxData : int = 0
    TxData : int = 0
    RxQoSData : int = 0
    TxQoSData : int = 0

class AP():
    def __init__(self, mac) -> None:
        self.info = APinfo(MAC=mac)

    def update_caps(self, caps):
        self.info.Capablity |= caps

    def get_caps(self):
        return self.info.Capablity

    def IncBeacon(self):
        self.info.BeaconSent += 1

    def QosDataTx(self):
        self.info.TxQoSData += 1

    def QosDataRx(self):
        self.info.RxQoSData +=1

class ap_list():
    def __init__(self):
        self.g_list = {}
        self.apCount = 0

    def AddAcessPoint(self, mac, ap):
        self.g_list.update({mac:ap})
        self.apCount += 1

    def FindAcessPoint(self, mac):
        return self.g_list.get(mac)

    def RemoveAP(self, mac):
        del self.g_list[mac]
        self.apCount -= 1

    def echoStats(self):
        logging.info("---------- PER AP STATS ----------")
        for mac, ap in self.g_list.items():
            logging.info("MAC ADDRESS       : %s", mac)
            logging.info("BEACON COUNT      : %d", ap.info.BeaconSent)
            logging.info("DATA TX           : %d", ap.info.TxData)
            logging.info("DATA RX           : %d", ap.info.RxData)
            logging.info("QOS DATA TX       : %d", ap.info.TxQoSData)
            logging.info("QOS DATA RX       : %d", ap.info.RxQoSData)

g_ap_list = ap_list()