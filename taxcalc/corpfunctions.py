"""
pitaxcalc-demo functions that calculate corporate income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit


@iterate_jit(nopython=True)
def net_tax_liability_a(NET_TAX_LIABILTY, NET_TAX_LIABILITY_B,
                        citax_rescale_rate):
    """
    Spit out tax liability (placeholder)
    """
    # TODO: replace this function with something else
    NET_TAX_LIABILITY_A = NET_TAX_LIABILTY * citax_rescale_rate
    return NET_TAX_LIABILITY_A


def net_tax_liability_b(calc):
    """
    Spit out tax liability (placeholder)
    """
    # TODO: replace this function with something else
    NET_TAX_LIABILITY = calc.carray('NET_TAX_LIABILTY')
    citax_rescale_rate = calc.policy_param('citax_rescale_rate')
    TAX2 = NET_TAX_LIABILITY * citax_rescale_rate
    calc.carray('NET_TAX_LIABILITY_B', TAX2)
