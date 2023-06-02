def get_mgmt_field(frame, field):
    return frame['WLAN.MGT'].get_field_value(field)

def all_mgmt_field(frame):
    return frame["WLAN.MGT"]._all_fields

def mgmt_get_diag_token(frame):
    return int(get_mgmt_field(frame, "wlan.fixed.dialog_token"), 16)

def mgmt_get_amsdu_support(frame):
    amsdu_support = frame['WLAN.MGT'].get_field_value("wlan.fixed.baparams.amsdu")
    return int(amsdu_support, 16)

def mgmt_get_ba_policy(frame):
    ba_policy = frame['WLAN.MGT'].get_field_value("wlan.fixed.baparams.policy")
    return int(ba_policy, 16)

def mgmt_get_tid(frame):
    return int(get_mgmt_field(frame, "wlan.fixed.baparams.tid"), 16)

def mgmt_get_buffer_size(frame):
    return int(get_mgmt_field(frame, "wlan.fixed.baparams.buffersize"), 16)

def mgmt_get_sequence_start(frame):
    return int(get_mgmt_field(frame, "wlan.fixed.ssc"), 16)