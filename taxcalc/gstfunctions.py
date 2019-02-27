"""
pitaxcalc-demo functions that calculate GST paid.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit


@iterate_jit(nopython=True)
def agg_consumption(CONS_CEREAL, CONS_OTHER, total_consumption):
    """
    Calculates the total Consumption of the individual
    """
    total_consumption = CONS_CEREAL + CONS_OTHER
    return total_consumption


@iterate_jit(nopython=True)
def gst_liability_cereal(gst_rate_cereal, CONS_CEREAL, gst_cereal):
    """
    Calculates the gst paid on Cereal consumption
    """
    gst_cereal = gst_rate_cereal * CONS_CEREAL
    return gst_cereal

"""
@iterate_jit(nopython=True)
def gst_liability_other(gst_rate_other, CONS_OTHER, gst_other):
    
    #Calculates the gst paid on Other consumption
    
    gst_other = gst_rate_other * CONS_OTHER
    return gst_other
"""

def gst_liability_other(calc):
    CONS_OTHER = calc.garray('CONS_OTHER')
    gst_rate_other = calc.policy_param('gst_rate_other')
    gst_other = gst_rate_other * CONS_OTHER
    calc.garray('gst_other', gst_other)
   

@iterate_jit(nopython=True)
def gst_liability(gst_cereal, gst_other, gst):
    """
    Compute total GST liability by adding up the GST on the components
    of consumption
    """
    gst = gst_cereal + gst_other
    return gst
