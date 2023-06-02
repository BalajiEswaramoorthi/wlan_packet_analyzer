from wlan import *
from mgmt import *
from enum import IntEnum
import logging
from AccessPoint import *
from station import *
from ActionFrame import ActionFrame
from dataclasses import dataclass

class subtype(IntEnum):
    ASSOC_REQ = 0
    ASSOC_RESP = 1
    REASSOC_REQ = 2
    REASSOC_RESP = 3
    PROBE_REQ = 4
    PROBE_RESP = 5
    BEACON = 8
    DISASSOC = 10
    AUTH = 11
    DEAUTH = 12
    ACTION = 13

@dataclass
class ManagementFrameStats():
    assocRequest: int = 0
    assocResponse: int = 0
    reAssocRequest: int = 0
    reAssocResponse: int = 0
    probeRequest: int = 0
    probeResponse: int = 0
    beaconFrame: int = 0
    disAssoc: int = 0
    authentication: int = 0
    deAuthentication: int = 0
    action: int = 0

class ManagementFrame():
    def __init__(self) -> None:
        self.assoc_sta_count = 0
        self.assoc_failure = 0

        self.stats = ManagementFrameStats()

        self.action_handler = ActionFrame()

    def echoStats(self):
        logging.info("ASSOC_REQ             = %d", self.stats.assocRequest)
        logging.info("ASSOC_RESP            = %d", self.stats.assocResponse)
        logging.info("REASSOC_REQ           = %d", self.stats.reAssocRequest)
        logging.info("REASSOC_RESP          = %d", self.stats.reAssocResponse)
        logging.info("PROBE_REQ             = %d", self.stats.probeRequest)
        logging.info("PROBE_RESP            = %d", self.stats.probeResponse)
        logging.info("BEACON                = %d", self.stats.beaconFrame)
        logging.info("DISASSOC              = %d", self.stats.disAssoc)
        logging.info("AUTH                  = %d", self.stats.authentication)
        logging.info("DEAUTH                = %d", self.stats.deAuthentication)
        logging.info("ACTION                = %d", self.stats.action)
        self.action_handler.echoStats()

    def AssociationRequest(self, frame):
        self.stats.assocRequest += 1

    def AssociationResponse(self, frame):
        self.stats.assocResponse += 1

    def ReassociationRequest(self, frame):
        self.stats.reAssocRequest += 1

    def ReassociationResponse(self, frame):
        self.stats.reAssocResponse += 1

    def ProbeRequest(self, frame):
        mac = wlan_field(frame, "wlan.ta")
        sta = g_sta_list.FindSta(mac)
        if (not sta):
            sta = station(mac)
            g_sta_list.add_sta(mac, sta)
            logging.info("Adding STA %s", mac)
        self.stats.probeRequest += 1

    def ProbeResponse(self, frame):
        self.stats.probeResponse += 1

    def BeaconFrame(self, frame):
        mac = wlan_field(frame, "wlan.ta")
        ap = g_ap_list.FindAcessPoint(mac)
        if (not ap):
            logging.info("Adding AP %s", mac)
            ap = AP(mac)
            g_ap_list.AddAcessPoint(mac, ap)
        ap.IncBeacon()
        self.stats.beaconFrame += 1

    def DisAssociation(self, frame):
        self.stats.disAssoc += 1

    def Authentication(self, frame):
        auth_seq = get_mgmt_field(frame, "wlan.fixed.auth_seq")
        if (int(auth_seq, 16) == 1):
            mac = wlan_field(frame, "wlan.ta")
            sta = g_sta_list.FindSta(mac)
            ap = g_ap_list.FindAcessPoint(mac)
            if (not (ap or sta)):
                sta = station(mac)
                g_sta_list.add_sta(mac, sta)
                logging.info("Adding STA %s", mac)
        elif (int(auth_seq, 16) == 2):
            pass
        self.stats.authentication += 1

    def Deauthentication(self, frame):
        self.stats.deAuthentication += 1

    def Action(self, frame):
        self.stats.action += 1
        self.action_handler.handle_action_frame(frame)

    def mgmt_handle(self, frame):
        #print(frame["WLAN"]._all_fields)
        frame_type = wlan_field_int(frame, "wlan.fc.type_subtype")
        match frame_type:
            case subtype.ASSOC_REQ:
                self.AssociationRequest(frame)
            case subtype.ASSOC_RESP:
                self.AssociationResponse(frame)
            case subtype.REASSOC_REQ:
                self.ReassociationRequest(frame)
            case subtype.REASSOC_RESP:
                self.ReassociationResponse(frame)
            case subtype.PROBE_REQ:
                self.ProbeRequest(frame)
            case subtype.PROBE_RESP:
                self.ProbeResponse(frame)
            case subtype.BEACON:
                self.BeaconFrame(frame)
            case subtype.DISASSOC:
                self.DisAssociation(frame)
            case subtype.AUTH:
                self.Authentication(frame)
            case subtype.DEAUTH:
                self.Deauthentication(frame)
            case subtype.ACTION:
                self.Action(frame)
            case _:
                logging.error("invalid management frame %d", frame_type)