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
def total_other_income(TOTAL_INCOME_OS):
    """
    Compute other_income from its components.
    """
    # TODO: when components of other income are available, do the calculation
    # TODO: when using other_income as function argument, no calculations neeed
    return TOTAL_INCOME_OS


@iterate_jit(nopython=True)
def gross_total_income(SALARIES, INCOME_HP, TOTAL_PROFTS_GAINS_BP,
                       ST_CG_AMT_APPRATE, TOTAL_INCOME_OS, GTI):
    """
    Compute GTI.
    """
    GTI = (SALARIES + INCOME_HP + TOTAL_PROFTS_GAINS_BP + ST_CG_AMT_APPRATE +
           TOTAL_INCOME_OS)
    return GTI


@iterate_jit(nopython=True)
def itemized_deductions(deductions):
    """
    Compute deductions from itemizeable expenses and caps.
    """
    # TODO: when expenses and caps policy are available, do the calculation
    # TODO: when using deductions as function argument, no calculations neeed
    return deductions


@iterate_jit(nopython=True)
def taxable_total_income(GTI, deductions, TTI):
    """
    Compute TTI.
    """
    TTI = GTI - deductions
    return TTI

def tax_stcg_splrate(calc):
    """
    Calculates the tax on short term capital gains which are taxed at spl rate
    Short term capital gain tax at applicable rate is included in tax on GTI.
    """
    ST_CG_RATE1 = calc.policy_param('ST_CG_RATE1')
    ST_CG_RATE2 = calc.policy_param('ST_CG_RATE2')
    ST_CG_AMT_1 = calc.array('ST_CG_AMT_1')
    ST_CG_AMT_2 = calc.array('ST_CG_AMT_2')
    tax_TI_special_rates = calc.array('tax_TI_special_rates')
    Tax_ST_CG_RATE1 = ST_CG_AMT_1 * ST_CG_RATE1
    Tax_ST_CG_RATE2 = ST_CG_AMT_2 * ST_CG_RATE2
    Total_Tax_STCG = Tax_ST_CG_RATE1 + Tax_ST_CG_RATE2
    calc.array('Tax_ST_CG_RATE1', Tax_ST_CG_RATE1)
    calc.array('Tax_ST_CG_RATE2', Tax_ST_CG_RATE2)
    calc.array('Total_Tax_STCG', Total_Tax_STCG)
    tax_TI_special_rates += Total_Tax_STCG
    calc.array('tax_TI_special_rates', tax_TI_special_rates)

def tax_ltcg_splrate(calc):
    """
    Calculates the tax on long term capital gains which are taxed at spl rates
    """
    LT_CG_RATE1 = calc.policy_param('LT_CG_RATE1')
    LT_CG_RATE2 = calc.policy_param('LT_CG_RATE2')
    LT_CG_AMT_1 = calc.array('LT_CG_AMT_1')
    LT_CG_AMT_2 = calc.array('LT_CG_AMT_2')
    tax_TI_special_rates = calc.array('tax_TI_special_rates')
    Tax_LT_CG_RATE1 = LT_CG_AMT_1 * LT_CG_RATE1
    Tax_LT_CG_RATE2 = LT_CG_AMT_2 * LT_CG_RATE2
    Total_Tax_LTCG = Tax_LT_CG_RATE1 + Tax_LT_CG_RATE2
    calc.array('Tax_LT_CG_RATE1', Tax_LT_CG_RATE1)
    calc.array('Tax_LT_CG_RATE2', Tax_LT_CG_RATE2)
    calc.array('Total_Tax_LTCG', Total_Tax_LTCG)
    tax_TI_special_rates += Total_Tax_LTCG
    calc.array('tax_TI_special_rates', tax_TI_special_rates)



def pit_liability(calc):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    taxinc = np.maximum(0., calc.array('TTI'))
    AGEGRP = calc.array('AGEGRP')
    rate1 = calc.policy_param('rate1')
    rate2 = calc.policy_param('rate2')
    rate3 = calc.policy_param('rate3')
    rate4 = calc.policy_param('rate4')
    tbrk1 = calc.policy_param('tbrk1')[AGEGRP]
    tbrk2 = calc.policy_param('tbrk2')
    tbrk3 = calc.policy_param('tbrk3')
    tbrk4 = calc.policy_param('tbrk4')
    rebate_rate = calc.policy_param('rebate_rate')
    rebate_thd = calc.policy_param('rebate_thd')
    rebate_ceiling = calc.policy_param('rebate_ceiling')
    surcharge_rate = calc.policy_param('surcharge_rate')
    surcharge_thd = calc.policy_param('surcharge_thd')
    rebate = np.where(taxinc > rebate_thd, 0.,
                      np.minimum(rebate_rate * taxinc, rebate_ceiling))
    calc.array('rebate', rebate)
    tax_normal_rates = (rate1 * np.minimum(taxinc, tbrk1) +
                        rate2 * np.minimum(tbrk2 - tbrk1,
                                           np.maximum(0., taxinc - tbrk1)) +
                        rate3 * np.minimum(tbrk3 - tbrk2,
                                           np.maximum(0., taxinc - tbrk2)) +
                        rate4 * np.maximum(0., taxinc - tbrk3))
    tax_TI_special_rates = calc.array('tax_TI_special_rates')
    tax = tax_normal_rates + tax_TI_special_rates
    calc.array('tax_TTI', tax)
    tax = np.where(rebate > tax, 0, tax - rebate)
    surcharge = np.where(taxinc > surcharge_thd, tax * surcharge_rate, 0.)
    calc.array('surcharge', surcharge)
    tax = tax + surcharge
    calc.array('pitax', tax)
