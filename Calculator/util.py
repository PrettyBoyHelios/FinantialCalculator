import simplejson as json
import numpy as np
from .models import Alternative


def get_data(alternative):
    np_ea = json.loads(alternative.earnings)
    np_op = json.loads(alternative.operative_costs)

    np_ea = get_array(alternative.earnings, alternative.n_periods)
    np_op = get_array(alternative.operative_costs, alternative.n_periods)

    net_flux = np_ea + np_op
    net_flux[alternative.n_periods-1] -= float(alternative.investment) * float(alternative.investment_payback) / 100
    net_flux = np.insert(net_flux,0, alternative.investment)
    #print("Net flux: ", net_flux)
    return net_flux

def get_flux(alternative):
    np_ea = json.loads(alternative.earnings)
    np_op = json.loads(alternative.operative_costs)

    np_ea = get_array(alternative.earnings, alternative.n_periods)
    np_op = get_array(alternative.operative_costs, alternative.n_periods)
    return np_ea, np_op


def get_array(flux, periods):
    mp_array = json.loads(flux)
    if len(mp_array) == 1:
        return np.array([mp_array[0] for i in range(0, periods)])
    elif len(mp_array) == periods:
        return np.array(mp_array)
    else:
        return np.zeros(0)


def clean_data(alt_string):
    alt_string = alt_string.replace(" ", "")
    alt_string = alt_string.replace("[", "")
    alt_string = alt_string.replace("]", "")
    split_op = alt_string.split(",")
    #print("split", split_op)
    num_split = [round(float(x), 2) for x in split_op]
    return json.dumps(num_split)