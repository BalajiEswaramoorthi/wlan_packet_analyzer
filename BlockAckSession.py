import logging
from dataclasses import dataclass

@dataclass
class BaSessionInfo:
    baPolicyReq: int = 0
    baPolicy: int = 0
    tid: int = -1
    bufferSizeReq: int = 0
    bufferSize: int = 0
    amsduSupportReq: int = 0
    amsduSupport: int = 0
    diagToken: int = 0
    delSession: bool = False
    isStarted: bool = False

class BaSession():
    def __init__(self, tid):
        self.info = BaSessionInfo(tid = tid)

    def DelBaSession(self):
        self.info.delSession = True
        self.info.isStarted = False

    def BaRequest(self, bufferSize, amsduSupport, baPolicy):
        self.info.baPolicyReq = baPolicy
        self.info.bufferSizeReq = bufferSize
        self.info.amsduSupportReq = amsduSupport

    def BaResponse(self, bufferSize, amsduSupport, baPolicy):
        self.info.bufferSize = bufferSize
        self.info.amsduSupport = amsduSupport
        self.info.baPolicy = baPolicy

    def BaSessionStart(self):
        self.info.isStarted = True

    def BaSessionInfo(self):
        logging.info("TID                   : %d", self.info.tid)
        logging.info("DIAG TOKEN            : %d", self.info.diagToken)
        logging.info("BA POLICY REQ         : %d", self.info.baPolicyReq)
        logging.info("BA POLICY             : %d", self.info.baPolicy)
        logging.info("AMSDU SUPPORT REQ     : %d", self.info.amsduSupportReq)
        logging.info("AMSDU SUPPORT         : %d", self.info.amsduSupport)
        logging.info("BUFFER SIZE REQ       : %d", self.info.bufferSizeReq)
        logging.info("BUFFER SIZE           : %d", self.info.bufferSize)