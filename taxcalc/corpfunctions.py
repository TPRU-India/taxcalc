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


@iterate_jit(nopython=True)
def corp_GTI(INCOME_HP, Income_BP, ST_CG_AMT_1, ST_CG_AMT_2, ST_CG_AMT_APPRATE,
             LT_CG_AMT_1, LT_CG_AMT_2, TOTAL_INCOME_OS, CY_Losses, BF_Losses,
             GTI):
    """
    Compute GTI including capital gains amounts taxed at special rates.
    """
    GTI = (INCOME_HP + Income_BP + ST_CG_AMT_1 + ST_CG_AMT_2 +
           ST_CG_AMT_APPRATE + LT_CG_AMT_1 + LT_CG_AMT_2 +
           TOTAL_INCOME_OS) - (CY_Losses + BF_Losses)
    GTI = np.maximum(0., GTI)
    return GTI


def net_tax_liability_b(calc):
    """
    Spit out tax liability (placeholder)
    """
    # TODO: replace this function with something else
    NET_TAX_LIABILITY = calc.carray('NET_TAX_LIABILTY')
    citax_rescale_rate = calc.policy_param('citax_rescale_rate')
    TAX2 = NET_TAX_LIABILITY * citax_rescale_rate
    calc.carray('NET_TAX_LIABILITY_B', TAX2)
