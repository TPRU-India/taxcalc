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
def corp_GTI_before_set_off(INCOME_HP, Income_BP, ST_CG_AMT_1, ST_CG_AMT_2,
                            ST_CG_AMT_APPRATE, LT_CG_AMT_1, LT_CG_AMT_2,
                            TOTAL_INCOME_OS, GTI_Before_Loss):
    """
    Compute GTI including capital gains amounts taxed at special rates.
    """
    GTI_Before_Loss = (INCOME_HP + Income_BP + ST_CG_AMT_1 + ST_CG_AMT_2 +
                       ST_CG_AMT_APPRATE + LT_CG_AMT_1 + LT_CG_AMT_2 +
                       TOTAL_INCOME_OS)
    return GTI_Before_Loss


@iterate_jit(nopython=True)
def GTI_and_losses(Loss_CFLimit, GTI_Before_Loss, CY_Losses,
                   LOSS_LAG1, LOSS_LAG2, LOSS_LAG3, LOSS_LAG4,
                   LOSS_LAG5, LOSS_LAG6, LOSS_LAG7, LOSS_LAG8,
                   GTI, newloss1, newloss2, newloss3, newloss4,
                   newloss5, newloss6, newloss7, newloss8):
    LOSS_LAGS = [LOSS_LAG1, LOSS_LAG2, LOSS_LAG3, LOSS_LAG4, LOSS_LAG5,
                 LOSS_LAG6, LOSS_LAG7, LOSS_LAG8]
    GTI1 = max(GTI_Before_Loss - CY_Losses, 0.)
    newloss1 = GTI1 - GTI_Before_Loss + CY_Losses
    USELOSS = np.zeros(8)
    for i in range(8, 0, -1):
        if Loss_CFLimit >= i:
            USELOSS[i-1] = min(GTI1, LOSS_LAGS[i-1])
        GTI1 = GTI1 - USELOSS[i-1]
    NETLOSSES = np.array(LOSS_LAGS) - USELOSS
    (newloss2, newloss3, newloss4, newloss5, newloss6,
     newloss7, newloss8) = NETLOSSES[:7]
    GTI = GTI1
    return (GTI, newloss1, newloss2, newloss3, newloss4,
            newloss5, newloss6, newloss7, newloss8)


def net_tax_liability_b(calc):
    """
    Spit out tax liability (placeholder)
    """
    # TODO: replace this function with something else
    NET_TAX_LIABILITY = calc.carray('NET_TAX_LIABILTY')
    citax_rescale_rate = calc.policy_param('citax_rescale_rate')
    TAX2 = NET_TAX_LIABILITY * citax_rescale_rate
    calc.carray('NET_TAX_LIABILITY_B', TAX2)
