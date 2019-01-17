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


@iterate_jit(nopython=True)
def cit_liability(cit_rate, cit_surcharge_rate, cit_surcharge_thd, cess_rate,
                  TTI, TI_special_rates, tax_TI_special_rates,
                  Aggregate_Income, tax_Aggregate_Income,
                  Total_Tax_Cap_Gains, Total_Tax_STCG, Total_Tax_LTCG, tax_TTI,
                  surcharge, cess, citax):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)

    Subtract 'TI_special_rates' from 'TTI' to get the portion of total income
    that is taxed at normal rates. Now add agricultural income (income used for
    rate purpose only) to get Aggregate_Income.
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = TTI - TI_special_rates
    taxinc = max(0., taxinc)
    # Check this later
    Aggregate_Income = taxinc
    # calculate tax on taxable income subject to taxation at normal rates
    # NOTE: Tax_ST_CG_APPRATE is not calculated here because its stacking
    #       and scope assumptions have not been specified.  If it is ever
    #       calculated here, be sure to add it to Total_Tax_STCG variable.
    surcharge_rate1 = cit_surcharge_rate[0]
    surcharge_rate2 = cit_surcharge_rate[1]
    surcharge_rate3 = cit_surcharge_rate[2]
    surcharge_thd1 = cit_surcharge_thd[0]
    surcharge_thd2 = cit_surcharge_thd[1]
    # compute tax on income taxed at normal rates
    tax_normal_rates = cit_rate * taxinc
    tax_Aggregate_Income = tax_normal_rates
    # compute tax_TTI
    tax_TTI = tax_normal_rates + tax_TI_special_rates
    tax = tax_TTI
    # compute surcharge amount
    if TTI < surcharge_thd1:
        surcharge = tax * surcharge_rate1
    else:
        if TTI >= surcharge_thd1 and TTI < surcharge_thd2:
            surcharge = tax * surcharge_rate2
        else:
            surcharge = tax * surcharge_rate3
    tax += surcharge
    # compute cess amount
    cess = tax * cess_rate
    # compute pitax amount
    citax = tax + cess
    Total_Tax_Cap_Gains = Total_Tax_STCG + Total_Tax_LTCG
    return (Aggregate_Income, tax_Aggregate_Income, tax_TTI,
            Total_Tax_Cap_Gains, surcharge, cess, citax)
