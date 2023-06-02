import logging
from wlan import *
from dataclasses import dataclass

class subtype(IntEnum):
    BLOCK_ACK_REQ = 24
    BLOCK_ACK = 25
    PS_POLL = 26
    RTS = 27
    CTS = 28
    ACK = 29
    CF_END = 30

@dataclass
class ControlFrameStats():
    BlockAckReq: int = 0
    BlockAck: int = 0
    PsPoll: int = 0
    ReqToSend: int = 0
    ClearToSend: int = 0
    Ack: int = 0
    CFend: int = 0

class ControlFrame():
    def __init__(self) -> None:
        self.stats = ControlFrameStats()

    def echoStats(self):
        logging.info("BLOCK_ACK_REQ         = %d", self.stats.BlockAckReq)
        logging.info("BLOCK_ACK             = %d", self.stats.BlockAck)
        logging.info("PS_POLL               = %d", self.stats.PsPoll)
        logging.info("RTS                   = %d", self.stats.ReqToSend)
        logging.info("CTS                   = %d", self.stats.ClearToSend)
        logging.info("ACK                   = %d", self.stats.Ack)
        logging.info("CF_END                = %d", self.stats.CFend)

    def blockAckreq(self, frame):
        self.stats.BlockAckReq += 1

    def blockAck(self, frame):
        self.stats.BlockAck += 1

    def psPoll(self, frame):
        self.stats.PsPoll += 1

    def process_rts(self, frame):
        self.stats.ReqToSend += 1

    def process_cts(self, frame):
        self.stats.ClearToSend += 1

    def Ack(self, frame):
        self.stats.Ack += 1

    def cfEnd(self, frame):
        self.stats.CFend += 1

    def control_frame(self, frame):
        sub_type = wlan_field_int(frame, "wlan.fc.type_subtype")
        match sub_type:
            case subtype.BLOCK_ACK_REQ:
                self.blockAckreq(frame)
            case subtype.BLOCK_ACK:
                self.blockAck(frame)
            case subtype.PS_POLL:
                self.psPoll(frame)
            case subtype.RTS:
                self.process_rts(frame)
            case subtype.CTS:
                self.process_cts(frame)
            case subtype.ACK:
                self.Ack(frame)
            case subtype.CF_END:
                self.cfEnd(frame)