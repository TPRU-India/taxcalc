"""
Functions that calculate corporate income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle corpfunctions.py
# pylint --disable=locally-disabled corpfunctions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit


@iterate_jit(nopython=True)
def depreciation_PM15(dep_rate_pm15, PWR_DOWN_VAL_1ST_DAY_PY_15P,
                      PADDTNS_180_DAYS__MOR_PY_15P, PCR34_PY_15P,
                      PADDTNS_LESS_180_DAYS_15P, PCR7_PY_15P,
                      PEXP_INCURRD_TRF_ASSTS_15P, PCAP_GAINS_LOSS_SEC50_15P,
                      PADDTNL_DEPRECTN_ANY_4_15P, PADDTNL_DEPRECTN_ANY_7_15P,
                      PADDTNL_DEPRECTN_LESS_180_DAYS_15P):
    '''
    Schedule DPM of ITR-6 for A.Y. 2017-18
    '''
    amt_full_rate15 = (PWR_DOWN_VAL_1ST_DAY_PY_15P +
                       PADDTNS_180_DAYS__MOR_PY_15P - PCR34_PY_15P)
    amt_half_rate15 = PADDTNS_LESS_180_DAYS_15P - PCR7_PY_15P
    dep_amt_pm15 = amt_full_rate15 * dep_rate_pm15
    dep_amt_pm15 += amt_half_rate15 * (dep_rate_pm15 / 2)
    addl_dep15 = (PADDTNL_DEPRECTN_ANY_4_15P + PADDTNL_DEPRECTN_ANY_7_15P +
                  PADDTNL_DEPRECTN_LESS_180_DAYS_15P)
    dep_amt_pm15 += addl_dep15
    close_wdv_pm15 = (PWR_DOWN_VAL_1ST_DAY_PY_15P +
                      PADDTNS_180_DAYS__MOR_PY_15P - PCR34_PY_15P +
                      PADDTNS_LESS_180_DAYS_15P - PCR7_PY_15P - dep_amt_pm15)
    cap_gain_pm15 = (PCR34_PY_15P + PCR7_PY_15P - PWR_DOWN_VAL_1ST_DAY_PY_15P -
                     PADDTNS_180_DAYS__MOR_PY_15P -
                     PEXP_INCURRD_TRF_ASSTS_15P -
                     PADDTNS_LESS_180_DAYS_15P)
    # Consider unusual cases when Capital Gains is negative and block DNE
    if (PCAP_GAINS_LOSS_SEC50_15P >= 0):
        cap_gain_pm15 = max(0.0, cap_gain_pm15)
    return (dep_amt_pm15, close_wdv_pm15)


@iterate_jit(nopython=True)
def depreciation_PM30(dep_rate_pm30, PWR_DOWN_VAL_1ST_DAY_PY_30P,
                      PADDTNS_180_DAYS__MOR_PY_30P, PCR34_PY_30P,
                      PADDTNS_LESS_180_DAYS_30P, PCR7_PY_30P,
                      PEXP_INCURRD_TRF_ASSTS_30P, PCAP_GAINS_LOSS_SEC50_30P,
                      PADDTNL_DEPRECTN_ANY_4_30P, PADDTNL_DEPRECTN_ANY_7_30P,
                      PADDTNL_DEPRECTN_LESS_180_DAYS_30P):
    '''
    Schedule DPM of ITR-6 for A.Y. 2017-18
    '''
    amt_full_rate30 = (PWR_DOWN_VAL_1ST_DAY_PY_30P +
                       PADDTNS_180_DAYS__MOR_PY_30P - PCR34_PY_30P)
    amt_half_rate30 = PADDTNS_LESS_180_DAYS_30P - PCR7_PY_30P
    dep_amt_pm30 = amt_full_rate30 * dep_rate_pm30
    dep_amt_pm30 += amt_half_rate30 * (dep_rate_pm30 / 2)
    addl_dep30 = (PADDTNL_DEPRECTN_ANY_4_30P + PADDTNL_DEPRECTN_ANY_7_30P +
                  PADDTNL_DEPRECTN_LESS_180_DAYS_30P)
    dep_amt_pm30 += addl_dep30
    close_wdv_pm30 = (PWR_DOWN_VAL_1ST_DAY_PY_30P +
                      PADDTNS_180_DAYS__MOR_PY_30P - PCR34_PY_30P +
                      PADDTNS_LESS_180_DAYS_30P - PCR7_PY_30P - dep_amt_pm30)
    cap_gain_pm30 = (PCR34_PY_30P + PCR7_PY_30P - PWR_DOWN_VAL_1ST_DAY_PY_30P -
                     PADDTNS_180_DAYS__MOR_PY_30P -
                     PEXP_INCURRD_TRF_ASSTS_30P -
                     PADDTNS_LESS_180_DAYS_30P)
    # Consider unusual cases when Capital Gains is negative and block DNE
    if (PCAP_GAINS_LOSS_SEC50_30P >= 0):
        cap_gain_pm30 = max(0.0, cap_gain_pm30)
    return (dep_amt_pm30, close_wdv_pm30)


@iterate_jit(nopython=True)
def depreciation_PM40(dep_rate_pm40, PWR_DOWN_VAL_1ST_DAY_PY_40P,
                      PADDTNS_180_DAYS__MOR_PY_40P, PCR34_PY_40P,
                      PADDTNS_LESS_180_DAYS_40P, PCR7_PY_40P,
                      PEXP_INCURRD_TRF_ASSTS_40P, PCAP_GAINS_LOSS_SEC50_40P,
                      PADDTNL_DEPRECTN_ANY_4_40P, PADDTNL_DEPRECTN_ANY_7_40P,
                      PADDTNL_DEPRECTN_LESS_180_DAYS_40P):
    '''
    Schedule DPM of ITR-6 for A.Y. 2017-18
    '''
    amt_full_rate40 = (PWR_DOWN_VAL_1ST_DAY_PY_40P +
                       PADDTNS_180_DAYS__MOR_PY_40P - PCR34_PY_40P)
    amt_half_rate40 = PADDTNS_LESS_180_DAYS_40P - PCR7_PY_40P
    dep_amt_pm40 = amt_full_rate40 * dep_rate_pm40
    dep_amt_pm40 += amt_half_rate40 * (dep_rate_pm40 / 2)
    addl_dep40 = (PADDTNL_DEPRECTN_ANY_4_40P + PADDTNL_DEPRECTN_ANY_7_40P +
                  PADDTNL_DEPRECTN_LESS_180_DAYS_40P)
    dep_amt_pm40 += addl_dep40
    close_wdv_pm40 = (PWR_DOWN_VAL_1ST_DAY_PY_40P +
                      PADDTNS_180_DAYS__MOR_PY_40P - PCR34_PY_40P +
                      PADDTNS_LESS_180_DAYS_40P - PCR7_PY_40P - dep_amt_pm40)
    cap_gain_pm40 = (PCR34_PY_40P + PCR7_PY_40P - PWR_DOWN_VAL_1ST_DAY_PY_40P -
                     PADDTNS_180_DAYS__MOR_PY_40P -
                     PEXP_INCURRD_TRF_ASSTS_40P -
                     PADDTNS_LESS_180_DAYS_40P)
    # Consider unusual cases when Capital Gains is negative and block DNE
    if (PCAP_GAINS_LOSS_SEC50_40P >= 0):
        cap_gain_pm40 = max(0.0, cap_gain_pm40)
    return (dep_amt_pm40, close_wdv_pm40)


@iterate_jit(nopython=True)
def depreciation_PM50(dep_rate_pm50, PWR_DOWN_VAL_1ST_DAY_PY_50P,
                      PADDTNS_180_DAYS__MOR_PY_50P, PCR34_PY_50P,
                      PADDTNS_LESS_180_DAYS_50P, PCR7_PY_50P,
                      PEXP_INCURRD_TRF_ASSTS_50P, PCAP_GAINS_LOSS_SEC50_50P,
                      PADDTNL_DEPRECTN_ANY_4_50P, PADDTNL_DEPRECTN_ANY_7_50P,
                      PADDTNL_DEPRECTN_LESS_180_DAYS_50P):
    '''
    Schedule DPM of ITR-6 for A.Y. 2017-18
    '''
    amt_full_rate50 = (PWR_DOWN_VAL_1ST_DAY_PY_50P +
                       PADDTNS_180_DAYS__MOR_PY_50P - PCR34_PY_50P)
    amt_half_rate50 = PADDTNS_LESS_180_DAYS_50P - PCR7_PY_50P
    dep_amt_pm50 = amt_full_rate50 * dep_rate_pm50
    dep_amt_pm50 += amt_half_rate50 * (dep_rate_pm50 / 2)
    addl_dep50 = (PADDTNL_DEPRECTN_ANY_4_50P + PADDTNL_DEPRECTN_ANY_7_50P +
                  PADDTNL_DEPRECTN_LESS_180_DAYS_50P)
    dep_amt_pm50 += addl_dep50
    close_wdv_pm50 = (PWR_DOWN_VAL_1ST_DAY_PY_50P +
                      PADDTNS_180_DAYS__MOR_PY_50P - PCR34_PY_50P +
                      PADDTNS_LESS_180_DAYS_50P - PCR7_PY_50P - dep_amt_pm50)
    cap_gain_pm50 = (PCR34_PY_50P + PCR7_PY_50P - PWR_DOWN_VAL_1ST_DAY_PY_50P -
                     PADDTNS_180_DAYS__MOR_PY_50P -
                     PEXP_INCURRD_TRF_ASSTS_50P -
                     PADDTNS_LESS_180_DAYS_50P)
    # Consider unusual cases when Capital Gains is negative and block DNE
    if (PCAP_GAINS_LOSS_SEC50_50P >= 0):
        cap_gain_pm50 = max(0.0, cap_gain_pm50)
    return (dep_amt_pm50, close_wdv_pm50)


@iterate_jit(nopython=True)
def depreciation_PM60(dep_rate_pm60, PWR_DOWN_VAL_1ST_DAY_PY_60P,
                      PADDTNS_180_DAYS__MOR_PY_60P, PCR34_PY_60P,
                      PADDTNS_LESS_180_DAYS_60P, PCR7_PY_60P,
                      PEXP_INCURRD_TRF_ASSTS_60P, PCAP_GAINS_LOSS_SEC50_60P,
                      PADDTNL_DEPRECTN_ANY_4_60P, PADDTNL_DEPRECTN_ANY_7_60P,
                      PADDTNL_DEPRECTN_LESS_180_DAYS_60P):
    '''
    Schedule DPM of ITR-6 for A.Y. 2017-18
    '''
    amt_full_rate60 = (PWR_DOWN_VAL_1ST_DAY_PY_60P +
                       PADDTNS_180_DAYS__MOR_PY_60P - PCR34_PY_60P)
    amt_half_rate60 = PADDTNS_LESS_180_DAYS_60P - PCR7_PY_60P
    dep_amt_pm60 = amt_full_rate60 * dep_rate_pm60
    dep_amt_pm60 += amt_half_rate60 * (dep_rate_pm60 / 2)
    addl_dep60 = (PADDTNL_DEPRECTN_ANY_4_60P + PADDTNL_DEPRECTN_ANY_7_60P +
                  PADDTNL_DEPRECTN_LESS_180_DAYS_60P)
    dep_amt_pm60 += addl_dep60
    close_wdv_pm60 = (PWR_DOWN_VAL_1ST_DAY_PY_60P +
                      PADDTNS_180_DAYS__MOR_PY_60P - PCR34_PY_60P +
                      PADDTNS_LESS_180_DAYS_60P - PCR7_PY_60P - dep_amt_pm60)
    cap_gain_pm60 = (PCR34_PY_60P + PCR7_PY_60P - PWR_DOWN_VAL_1ST_DAY_PY_60P -
                     PADDTNS_180_DAYS__MOR_PY_60P -
                     PEXP_INCURRD_TRF_ASSTS_60P -
                     PADDTNS_LESS_180_DAYS_60P)
    # Consider unusual cases when Capital Gains is negative and block DNE
    if (PCAP_GAINS_LOSS_SEC50_60P >= 0):
        cap_gain_pm60 = max(0.0, cap_gain_pm60)
    return (dep_amt_pm60, close_wdv_pm60)


@iterate_jit(nopython=True)
def depreciation_PM80(dep_rate_pm80, PWR_DOWN_VAL_1ST_DAY_PY_80P,
                      PADDTNS_180_DAYS__MOR_PY_80P, PCR34_PY_80P,
                      PADDTNS_LESS_180_DAYS_80P, PCR7_PY_80P,
                      PEXP_INCURRD_TRF_ASSTS_80P, PCAP_GAINS_LOSS_SEC50_80P,
                      PADDTNL_DEPRECTN_ANY_4_80P, PADDTNL_DEPRECTN_ANY_7_80P,
                      PADDTNL_DEPRECTN_LESS_180_DAYS_80P):
    '''
    Schedule DPM of ITR-6 for A.Y. 2017-18
    '''
    amt_full_rate80 = (PWR_DOWN_VAL_1ST_DAY_PY_80P +
                       PADDTNS_180_DAYS__MOR_PY_80P - PCR34_PY_80P)
    amt_half_rate80 = PADDTNS_LESS_180_DAYS_80P - PCR7_PY_80P
    dep_amt_pm80 = amt_full_rate80 * dep_rate_pm80
    dep_amt_pm80 += amt_half_rate80 * (dep_rate_pm80 / 2)
    addl_dep80 = (PADDTNL_DEPRECTN_ANY_4_80P + PADDTNL_DEPRECTN_ANY_7_80P +
                  PADDTNL_DEPRECTN_LESS_180_DAYS_80P)
    dep_amt_pm80 += addl_dep80
    close_wdv_pm80 = (PWR_DOWN_VAL_1ST_DAY_PY_80P +
                      PADDTNS_180_DAYS__MOR_PY_80P - PCR34_PY_80P +
                      PADDTNS_LESS_180_DAYS_80P - PCR7_PY_80P - dep_amt_pm80)
    cap_gain_pm80 = (PCR34_PY_80P + PCR7_PY_80P - PWR_DOWN_VAL_1ST_DAY_PY_80P -
                     PADDTNS_180_DAYS__MOR_PY_80P -
                     PEXP_INCURRD_TRF_ASSTS_80P -
                     PADDTNS_LESS_180_DAYS_80P)
    # Consider unusual cases when Capital Gains is negative and block DNE
    if (PCAP_GAINS_LOSS_SEC50_80P >= 0):
        cap_gain_pm80 = max(0.0, cap_gain_pm80)
    return (dep_amt_pm80, close_wdv_pm80)


@iterate_jit(nopython=True)
def depreciation_PM100(dep_rate_pm100, PWR_DOWN_VAL_1ST_DAY_PY_100P,
                       PADDTNS_180_DAYS__MOR_PY_100P, PCR34_PY_100P,
                       PADDTNS_LESS_180_DAYS_100P, PCR7_PY_100P,
                       PEXP_INCURRD_TRF_ASSTS_100P, PCAP_GAINS_LOSS_SEC50_100P,
                       PADDTNL_DEPRECTN_ANY_4_100P,
                       PADDTNL_DEPRECTN_ANY_7_100P,
                       PADDTNL_DEPRECTN_LESS_180_DAYS_100P):
    '''
    Schedule DPM of ITR-6 for A.Y. 2017-18
    '''
    amt_full_rate100 = (PWR_DOWN_VAL_1ST_DAY_PY_100P +
                        PADDTNS_180_DAYS__MOR_PY_100P - PCR34_PY_100P)
    amt_half_rate100 = PADDTNS_LESS_180_DAYS_100P - PCR7_PY_100P
    dep_amt_pm100 = amt_full_rate100 * dep_rate_pm100
    dep_amt_pm100 += amt_half_rate100 * (dep_rate_pm100 / 2)
    addl_dep100 = (PADDTNL_DEPRECTN_ANY_4_100P + PADDTNL_DEPRECTN_ANY_7_100P +
                   PADDTNL_DEPRECTN_LESS_180_DAYS_100P)
    dep_amt_pm100 += addl_dep100
    close_wdv_pm100 = (PWR_DOWN_VAL_1ST_DAY_PY_100P +
                       PADDTNS_180_DAYS__MOR_PY_100P - PCR34_PY_100P +
                       PADDTNS_LESS_180_DAYS_100P - PCR7_PY_100P -
                       dep_amt_pm100)
    cap_gain_pm100 = (PCR34_PY_100P + PCR7_PY_100P -
                      PWR_DOWN_VAL_1ST_DAY_PY_100P -
                      PADDTNS_180_DAYS__MOR_PY_100P -
                      PEXP_INCURRD_TRF_ASSTS_100P -
                      PADDTNS_LESS_180_DAYS_100P)
    # Consider unusual cases when Capital Gains is negative and block DNE
    if (PCAP_GAINS_LOSS_SEC50_100P >= 0):
        cap_gain_pm100 = max(0.0, cap_gain_pm100)
    return (dep_amt_pm100, close_wdv_pm100)


@iterate_jit(nopython=True)
def depreciation_PM(dep_amt_pm15, dep_amt_pm30, dep_amt_pm40, dep_amt_pm50,
                    dep_amt_pm60, dep_amt_pm80, dep_amt_pm100, dep_amt_pm):
    dep_amt_pm = (dep_amt_pm15 + dep_amt_pm30 + dep_amt_pm40 + dep_amt_pm50 +
                  dep_amt_pm60 + dep_amt_pm80 + dep_amt_pm100)
    return dep_amt_pm


@iterate_jit(nopython=True)
def corp_income_business_profession(dep_amt_pm, PRFT_GAIN_BP_OTHR_SPECLTV_BUS,
                                    PRFT_GAIN_BP_SPECLTV_BUS,
                                    PRFT_GAIN_BP_SPCFD_BUS,
                                    PRFT_GAIN_BP_INC_115BBF, Income_BP):
    """
    Compute Income from Business and Profession by adding the different
    sub-heads (i.e speculative, non-speculative, specified, patents, etc)
    """
    # TODO: when reading from schedule BP, calculate Income_BP from the read
    # TODO: variables of the schedule
    Income_BP = (PRFT_GAIN_BP_OTHR_SPECLTV_BUS + PRFT_GAIN_BP_SPECLTV_BUS +
                 PRFT_GAIN_BP_SPCFD_BUS + PRFT_GAIN_BP_INC_115BBF -
                 dep_amt_pm)
    return Income_BP


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

@iterate_jit(nopython=True)
def MAT_liability_and_credit(MAT_CFLimit, TAX_UNDER_SEC115JB_CURR_ASSTYR, citax, 
                             MAT_CR_CY, MAT_LAG1, MAT_LAG2, MAT_LAG3, MAT_LAG4,
                             MAT_LAG5, MAT_LAG6, MAT_LAG7, MAT_LAG8, MAT_LAG9, 
                             MAT_LAG10, NEW_MAT_CR1, NEW_MAT_CR2, NEW_MAT_CR3, NEW_MAT_CR4,
                             NEW_MAT_CR5, NEW_MAT_CR6, NEW_MAT_CR7, NEW_MAT_CR8,
                             NEW_MAT_CR9, NEW_MAT_CR10, MAT_UTIL, MAT_CF):
    
    MAT_CR_LAGS = [MAT_LAG1, MAT_LAG2, MAT_LAG3, MAT_LAG4, MAT_LAG5,
                   MAT_LAG6, MAT_LAG7, MAT_LAG8, MAT_LAG9, MAT_LAG10]
    
    NEW_MAT_CR = [NEW_MAT_CR1, NEW_MAT_CR2, NEW_MAT_CR3, 
                  NEW_MAT_CR4, NEW_MAT_CR5, NEW_MAT_CR6, NEW_MAT_CR7, 
                  NEW_MAT_CR8, NEW_MAT_CR9, NEW_MAT_CR10]
    
    citax_liability = max(TAX_UNDER_SEC115JB_CURR_ASSTYR, citax)
        
    if TAX_UNDER_SEC115JB_CURR_ASSTYR > citax:
        
        MAT_CR_CY = TAX_UNDER_SEC115JB_CURR_ASSTYR - citax
        NEW_MAT_CR[0] = MAT_CR_CY
        NEW_MAT_CR[1:10] = [NEW_MAT_CR1, NEW_MAT_CR2, NEW_MAT_CR3, 
                            NEW_MAT_CR4, NEW_MAT_CR5, NEW_MAT_CR6, NEW_MAT_CR7, 
                            NEW_MAT_CR8, NEW_MAT_CR9]
    else:
        
        USEMAT_CR = np.zeros(10)
        
        for i in range(10, 0, -1):
            if MAT_CFLimit >= i:
                USEMAT_CR[i-1] = min(citax_liability, MAT_CR_LAGS[i-1])
            citax_liability = citax_liability - USEMAT_CR[i-1]
        NETMAT_CR = np.array(MAT_CR_LAGS) - USEMAT_CR
        NEW_MAT_CR[1:10] = NETMAT_CR[:9]
        NEW_MAT_CR[0] = 0
        
    citax = citax_liability
    return (citax, USEMAT_CR, NEW_MAT_CR)
        
        
    