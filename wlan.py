import logging
from enum import IntEnum
import AccessPoint

class CAPS_BIT(IntEnum):
    HT = 0
    VHT = 1
    HE = 2
    EHT = 3
    ML = 4
class WLAN_CAPS(IntEnum):
    HT_CAPABLE = 1 << CAPS_BIT.HT
    VHT_CAPABLE = 1 << CAPS_BIT.VHT
    HE_CAPABLE = 1 << CAPS_BIT.HE
    EHT_CAPABLE = 1 << CAPS_BIT.EHT
    ML_CAPABLE = 1 << CAPS_BIT.ML

class type(IntEnum):
    MGMT = 0
    CONTROL = 1
    DATA = 2

def layers_in_packet(packet):
    return packet.layers

def get_frame_info(frame):
    return frame.frame_info

def wlan_field(frame, field):
    return frame["WLAN"].get_field_value(field)

def wlan_field_int(frame, field, ):
    return int(frame["WLAN"].get_field_value(field), 0)

def wlan_radio_field(frame, field):
    return frame["WLAN_RADIO"].get_field_value(field)

def wlan_info(frame):
    return frame["WLAN"]._all_fields

def wlan_radio_info(frame):
    return frame["WLAN_RADIO"]._all_fields