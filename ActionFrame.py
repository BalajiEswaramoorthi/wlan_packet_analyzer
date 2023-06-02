import logging
from enum import IntEnum
from AccessPoint import *
from station import *
from mgmt import *
from wlan import *

class CATEGORY(IntEnum):
    BLOCK_ACK = 3

class BA_ACTION_CODE(IntEnum):
    ADDBA_REQ = 0
    ADDBA_RESP = 1
    DELBA = 2

class ActionFrame():
    def __init__(self):
        self.addba_req = 0
        self.addba_resp = 0
        self.del_ba = 0

    def blockAck(self, frame):
        action_code = int(get_mgmt_field(frame, "wlan.fixed.action_code"), 16)
        if (action_code == BA_ACTION_CODE.ADDBA_REQ):
            self.addba_req += 1
            mac = wlan_field(frame, "wlan.ta")
            sta = g_sta_list.FindSta(mac)
            if (not sta):
                mac = wlan_field(frame, "wlan.ra")
                sta = g_sta_list.FindSta(mac)
                if (not sta):
                    logging.error("%s is not found in STA list", mac)
                    return
        elif (action_code == BA_ACTION_CODE.ADDBA_RESP):
            self.addba_resp += 1
        elif (action_code == BA_ACTION_CODE.DELBA):
            self.del_ba += 1

    def handle_action_frame(self, frame):
        if ("WLAN.MGT" in str(frame.layers)):
            category = int(get_mgmt_field(frame, "wlan.fixed.category_code"), 0)
            match category:
                case CATEGORY.BLOCK_ACK:
                    self.blockAck(frame)
            #print(frame["WLAN.MGT"]._all_fields)

    def echoStats(self):
        logging.info("ADDBA_REQ             = %d", self.addba_req)
        logging.info("ADDBA_RESP            = %d", self.addba_resp)
        logging.info("DELBA                 = %d", self.del_ba)