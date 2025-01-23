from devices import dragino_s31blb_ttn
from devices import mlsght_em320_ttn
from devices import my_custom_sensor

handlers_list = {
    "dragino_s31b-lb_ttn": dragino_s31blb_ttn.dragino_s31blb_ttn,
    "milesight-em320_ttn": mlsght_em320_ttn.mlsght_em320_ttn,
    "my_custom_sensor": my_custom_sensor.my_custom_sensor,
}
