import tempfile, logging, argparse, os, pyshark, signal

from mgmt_frame import ManagementFrame
import DataFrame
from ControlFrame import ControlFrame
from wlan import *
from AccessPoint import *
from station import *

KillSignalReceived = False

def PacketAnalyzerExit():
    logging.error("Kill Signal Received, Terminating")
    KillSignalReceived = True

if __name__ == '__main__':
    _nameToLevel = logging.getLevelNamesMapping()
    arg = argparse.ArgumentParser()

    arg.add_argument("pcap_file", nargs=1, action="store", type=str, help="pcap file that need to analyzed")
    arg.add_argument("--file_logging", action="store_true", help="enable file logging")
    arg.add_argument("--log_file", nargs=1, help="log file location")
    arg.add_argument("--log_level", nargs=1, choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], help="increase log verbosity")
    args = arg.parse_args()

    log_file = args.log_file
    file_logging = args.file_logging
    log_level = _nameToLevel.get(args.log_level[0])
    pcap = args.pcap_file[0]

    # file to save the log.
    if (file_logging and (not log_file)):
        log_file = os.path.join(tempfile.gettempdir(), "packet_analyzer.log")
        print(log_file)

    if (file_logging):
        logging.basicConfig(filename=log_file, filemode='w', datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(asctime)s %(module)-15s %(funcName)-20.20s %(lineno)4d [%(levelname)-s]: %(message)s',
                            level=log_level)
    else:
        logging.basicConfig(level=log_level, datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(asctime)s %(module)-15s %(funcName)-20.20s %(lineno)4d [%(levelname)-s]: %(message)s')

    mgmt = ManagementFrame()
    control = ControlFrame()
    data = DataFrame.dataFrame()

    logging.info("Registering kill signal handler")
    signal.signal(signal.SIGINT, PacketAnalyzerExit)
    signal.signal(signal.SIGTERM, PacketAnalyzerExit)

    path = os.path.join(os.getcwd(), pcap)
    tshark_path = os.path.join("C:\WFA\Wireshark", "tshark.exe")

    capture = pyshark.FileCapture(path, tshark_path=tshark_path)
    logging.info("ReadComplete")
    for frame in capture:
        if (KillSignalReceived):
            break
        if ("WLAN" in str(frame.layers)):
            frame_type = int(wlan_field(frame, "wlan.fc.type"), 0)
            #logging.debug("frame type %d", frame_type)
            match frame_type:
                case type.MGMT:
                    mgmt.mgmt_handle(frame)
                case type.CONTROL:
                    control.control_frame(frame)
                case type.DATA:
                    data.data_frame(frame)
                case _:
                    logging.error("unknown type %d", frame_type)
        else:
            logging.error("not a WLAN frame")

    logging.info("---------- STATS ----------")
    mgmt.echoStats()
    control.echoStats()
    data.echoStats()
    g_ap_list.echoStats()
    g_sta_list.echoStats()