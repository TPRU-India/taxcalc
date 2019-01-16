"""
pitaxcalc-demo functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit


@iterate_jit(nopython=True)
def net_salary_income(SALARIES):
    """
    Compute net salary as gross salary minus u/s 16 deductions.
    """
    # TODO: when gross salary and deductions are avaiable, do the calculation
    # TODO: when using net_salary as function argument, no calculations neeed
    return SALARIES


@iterate_jit(nopython=True)
def net_rental_income(INCOME_HP):
    """
    Compute house-property rental income net of taxes, depreciation, and
    mortgage interest.
    """
    # TODO: when gross rental income and taxes, depreciation, and interest
    #       are available, do the calculation
    # TODO: when using net_rent as function argument, no calculations neeed
    return INCOME_HP


@iterate_jit(nopython=True)
def income_business_profession(PRFT_GAIN_BP_OTHR_SPECLTV_BUS,
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
                 PRFT_GAIN_BP_SPCFD_BUS + PRFT_GAIN_BP_INC_115BBF)
    return Income_BP


@iterate_jit(nopython=True)
def total_other_income(TOTAL_INCOME_OS):
    """
    Compute other_income from its components.
    """
    # TODO: when components of other income are available, do the calculation
    # TODO: when using other_income as function argument, no calculations neeed
    return TOTAL_INCOME_OS


@iterate_jit(nopython=True)
def current_year_losses(CYL_SET_OFF, CY_Losses):
    """
    Compute Current Year Losses to be set off, from Schedule CYLA.
    """
    # TODO: when schedule is available, do the calculation
    # TODO: when reading CYL_SET_OFF from the data, no calculations neeed
    CY_Losses = CYL_SET_OFF
    return CY_Losses


@iterate_jit(nopython=True)
def brought_fwd_losses(BFL_SET_OFF_BALANCE, BF_Losses):
    """
    Compute Brought forward Losses to be set off, from Schedule BFLA.
    """
    # TODO: when schedule is available, do the calculation
    # TODO: when reading BFL_SET_OFF_BALANCE from the data, no calculations
    BF_Losses = BFL_SET_OFF_BALANCE
    return BF_Losses


@iterate_jit(nopython=True)
def agri_income(Income_Rate_Purpose, NET_AGRC_INCOME):
    """
    Compute the total Income that is used for rate purpose.
    It currently has only the net agricultural income.
    """
    # TODO: when shedule is available, do the calculation
    Income_Rate_Purpose = NET_AGRC_INCOME
    return Income_Rate_Purpose


@iterate_jit(nopython=True)
def gross_total_income(SALARIES, INCOME_HP, Income_BP, ST_CG_AMT_1,
                       ST_CG_AMT_2, ST_CG_AMT_APPRATE, LT_CG_AMT_1,
                       LT_CG_AMT_2, TOTAL_INCOME_OS, CY_Losses, BF_Losses,
                       GTI):
    """
    Compute GTI including capital gains amounts taxed at special rates.
    """
    GTI = (SALARIES + INCOME_HP + Income_BP + ST_CG_AMT_1 + ST_CG_AMT_2 +
           ST_CG_AMT_APPRATE + LT_CG_AMT_1 + LT_CG_AMT_2 +
           TOTAL_INCOME_OS) - (CY_Losses + BF_Losses)
    GTI = np.maximum(0., GTI)
    return GTI


@iterate_jit(nopython=True)
def itemized_deductions(deductions, TOTAL_DEDUC_VIA):
    """
    Compute deductions from itemizeable expenses and caps.
    """
    # TODO: when expenses and caps policy are available, do the calculation
    # TODO: when using deductions as function argument, no calculations neeed
    deductions = TOTAL_DEDUC_VIA
    return deductions


@iterate_jit(nopython=True)
def taxable_total_income(GTI, deductions, TTI):
    """
    Compute TTI.
    """
    TTI = GTI - deductions
    TTI = np.maximum(0., TTI)
    return TTI


@iterate_jit(nopython=True)
def tax_stcg_splrate(ST_CG_RATE1, ST_CG_RATE2, ST_CG_AMT_1, ST_CG_AMT_2):
    """
    Calculates the tax on short term capital gains which are taxed at spl rate
    Short term capital gain tax at applicable rate is included in tax on GTI.
    """
    Tax_ST_CG_RATE1 = ST_CG_AMT_1 * ST_CG_RATE1
    Tax_ST_CG_RATE2 = ST_CG_AMT_2 * ST_CG_RATE2
    Total_Tax_STCG = Tax_ST_CG_RATE1 + Tax_ST_CG_RATE2
    return (Tax_ST_CG_RATE1, Tax_ST_CG_RATE2, Total_Tax_STCG)


@iterate_jit(nopython=True)
def tax_ltcg_splrate(LT_CG_RATE1, LT_CG_RATE2, LT_CG_AMT_1, LT_CG_AMT_2):
    """
    Calculates the tax on long term capital gains which are taxed at spl rates
    """
    Tax_LT_CG_RATE1 = LT_CG_AMT_1 * LT_CG_RATE1
    Tax_LT_CG_RATE2 = LT_CG_AMT_2 * LT_CG_RATE2
    Total_Tax_LTCG = Tax_LT_CG_RATE1 + Tax_LT_CG_RATE2
    return (Tax_LT_CG_RATE1, Tax_LT_CG_RATE2, Total_Tax_LTCG)


@iterate_jit(nopython=True)
def tax_specialrates(ST_CG_AMT_1, ST_CG_AMT_2, LT_CG_AMT_1, LT_CG_AMT_2,
                     Total_Tax_STCG, Total_Tax_LTCG):
    """
    Calculates the total capital gains and tax on it
    which are taxed at spl rates
    """
    TI_special_rates = ST_CG_AMT_1 + ST_CG_AMT_2 + LT_CG_AMT_1 + LT_CG_AMT_2
    tax_TI_special_rates = Total_Tax_STCG + Total_Tax_LTCG
    return (TI_special_rates, tax_TI_special_rates)


DEBUG = False
DEBUG_IDX = 0


def pit_liability(calc):
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
    TTI = calc.array('TTI')
    taxinc = TTI - calc.array('TI_special_rates')
    taxinc = np.maximum(0., taxinc)
    agginc = taxinc + calc.array('Income_Rate_Purpose')
    agginc = np.maximum(0., agginc)

    calc.array('Aggregate_Income', taxinc)
    # calculate tax on taxable income subject to taxation at normal rates
    # NOTE: Tax_ST_CG_APPRATE is not calculated here because its stacking
    #       and scope assumptions have not been specified.  If it is ever
    #       calculated here, be sure to add it to Total_Tax_STCG variable.
    AGEGRP = calc.array('AGEGRP')
    rate1 = calc.policy_param('rate1')
    rate2 = calc.policy_param('rate2')
    rate3 = calc.policy_param('rate3')
    rate4 = calc.policy_param('rate4')
    tbrk1 = calc.policy_param('tbrk1')[AGEGRP]
    tbrk2 = calc.policy_param('tbrk2')[AGEGRP]
    tbrk3 = calc.policy_param('tbrk3')[AGEGRP]
    tbrk4 = calc.policy_param('tbrk4')[AGEGRP]
    rebate_rate = calc.policy_param('rebate_rate')
    rebate_thd = calc.policy_param('rebate_thd')
    rebate_ceiling = calc.policy_param('rebate_ceiling')
    surcharge_rate1 = calc.policy_param('surcharge_rate')[0]
    surcharge_rate2 = calc.policy_param('surcharge_rate')[1]
    surcharge_rate3 = calc.policy_param('surcharge_rate')[2]
    surcharge_thd1 = calc.policy_param('surcharge_thd')[0]
    surcharge_thd2 = calc.policy_param('surcharge_thd')[1]
    cess_rate = calc.policy_param('cess_rate')
    # compute tax on income taxed at normal rates
    tax_normal_rates = (rate1 * np.minimum(agginc, tbrk1) +
                        rate2 * np.minimum(tbrk2 - tbrk1,
                                           np.maximum(0., agginc - tbrk1)) +
                        rate3 * np.minimum(tbrk3 - tbrk2,
                                           np.maximum(0., agginc - tbrk2)) +
                        rate4 * np.maximum(0., agginc - tbrk3))
    calc.array('tax_Aggregate_Income', tax_normal_rates)
    # compute tax_TTI
    tax_TTI = tax_normal_rates + calc.array('tax_TI_special_rates')
    """
    Compute the rebate on agricultural income. Agricultural income is exempt
    but it is used for rate purpose.
    """
    agri_inc = calc.array('Income_Rate_Purpose') + tbrk1
    rebate_agri = (rate1 * np.minimum(agri_inc, tbrk1) +
                   rate2 * np.minimum(tbrk2 - tbrk1,
                                      np.maximum(0., agri_inc - tbrk1)) +
                   rate3 * np.minimum(tbrk3 - tbrk2,
                                      np.maximum(0., agri_inc - tbrk2)) +
                   rate4 * np.maximum(0., agri_inc - tbrk3))
    # Acricultural rebate only applicable if taxinc is greater than tbrk1
    rebate_agri = np.where(taxinc > tbrk1, rebate_agri, 0.)
    calc.array('rebate_agri', rebate_agri)
    # Acricultural rebate cannot be more than the tax liability
    rebate_agri = np.minimum(tax_TTI, calc.array('rebate_agri'))
    calc.array('rebate_agri', rebate_agri)
    # Update tax_TTI after allowing agricultural rebate
    tax_TTI -= rebate_agri
    calc.array('tax_TTI', tax_TTI)
    # Compute rebate amount u/s 87A. Only applicablle if TTI > rebate_thd
    rebate = np.where(TTI > rebate_thd, 0.,
                      np.minimum(rebate_rate * TTI, rebate_ceiling))
    # As rebate is a non-refundable credit it should capped to tax_TTI
    rebate = np.minimum(tax_TTI, rebate)
    calc.array('rebate', rebate)
    tax = tax_TTI - rebate
    # compute surcharge amount
    surcharge = np.where(taxinc < surcharge_thd1, taxinc * surcharge_rate1,
                         np.where((taxinc >= surcharge_thd1) &
                                  (taxinc < surcharge_thd2),
                                  taxinc * surcharge_rate2,
                                  taxinc * surcharge_rate3))
    calc.array('surcharge', surcharge)
    tax += surcharge
    # compute cess amount
    cess = tax * cess_rate
    calc.array('cess', cess)
    # compute pitax amount
    tax += cess
    calc.array('pitax', tax)
    # calculate Total_Tax_Cap_Gains
    calc.array('Total_Tax_Cap_Gains',
               calc.array('Total_Tax_STCG') + calc.array('Total_Tax_LTCG'))
