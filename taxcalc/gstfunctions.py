"""
pitaxcalc-demo functions that calculate GST paid.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import json
import numpy as np
from taxcalc.gstrecords import GSTRecords


def gst_liability_item(calc):
    vardict = GSTRecords.read_var_info()
    FIELD_VARS = list(k for k, v in vardict['read'].items()
                      if (v['type'] == 'int' or v['type'] == 'float'))
    total_consumption = np.zeros(len(calc.garray('CONS_CEREAL')))
    gst = np.zeros(len(calc.garray('CONS_CEREAL')))
    for v in FIELD_VARS:
        if v.startswith('CONS_'):
            w = v.replace('CONS_', 'gst_rate_').lower()
            x = v.replace('CONS_', 'gst_').lower()
            cons_item = calc.garray(v)
            gst_rate_item = calc.policy_param(w)
            gst_item = cons_item * gst_rate_item
            calc.garray(x, gst_item)
            total_consumption += cons_item
            gst += gst_item
    calc.garray('total consumption', total_consumption)
    calc.garray('gst', gst)
