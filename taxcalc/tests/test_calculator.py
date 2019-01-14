# CODING-STYLE CHECKS:
# pycodestyle test_calculator.py

import os
import json
from io import StringIO
import tempfile
import copy
import pytest
import numpy as np
import pandas as pd
from taxcalc import Policy, Records, Calculator


def test_incorrect_Calculator_instantiation(pit_subsample):
    pol = Policy()
    rec = Records(data=pit_subsample)
    with pytest.raises(ValueError):
        Calculator(policy=None, records=rec)
    with pytest.raises(ValueError):
        Calculator(policy=pol, records=None)
    with pytest.raises(ValueError):
        Policy(num_years=0)


def test_correct_Calculator_instantiation(pit_fullsample, pit_subsample):
    syr = Policy.JSON_START_YEAR
    pol = Policy()
    assert pol.current_year == syr
    # specify expected number of filers and aggregate PIT liability
    expect_weight = 35.241e6
    expect_pitax = 1822.119e9
    # create full-sample Calculator object
    rec_full = Records(data=pit_fullsample)
    calc_full = Calculator(policy=pol, records=rec_full)
    assert isinstance(calc_full, Calculator)
    assert calc_full.current_year == syr
    assert calc_full.records_current_year() == syr
    calc_full.calc_all()
    actual_full_weight = calc_full.total_weight()
    actual_full_pitax = calc_full.weighted_total('pitax')
    assert np.allclose([actual_full_weight], [expect_weight])
    assert np.allclose([actual_full_pitax], [expect_pitax])
    # create sub-sample Calculator object
    """
    rec_sub = Records(data=pit_subsample)
    calc_sub = Calculator(policy=pol, records=rec_sub)
    calc_sub.calc_all()
    actual_sub_weight = calc_sub.total_weight()
    actual_sub_pitax = calc_sub.weighted_total('pitax')
    assert np.allclose([actual_sub_weight], [expect_weight])
    assert np.allclose([actual_sub_pitax], [expect_pitax], rtol=0.07)
    """


def test_Calculator_results_consistency(pit_fullsample):
    # generate calculated-variable dataframe for full sample in second year
    recs = Records(data=pit_fullsample)
    calc = Calculator(policy=Policy(), records=recs)
    assert isinstance(calc, Calculator)
    assert calc.current_year == Policy.JSON_START_YEAR
    calc.advance_to_year(Policy.JSON_START_YEAR + 1)
    assert calc.current_year == Policy.JSON_START_YEAR + 1
    calc.calc_all()
    varlist = list(Records.CALCULATED_VARS)
    vdf = calc.dataframe(varlist)
    assert isinstance(vdf, pd.DataFrame)
    # check consistency of calculated results individual by individual
    assert np.allclose(vdf['TTI'],
                       vdf['GTI'] - vdf['deductions'])
    assert np.allclose(vdf['Aggregate_Income'],
                       vdf['TTI'] - vdf['TI_special_rates'])
    assert np.all(vdf['Tax_ST_CG_RATE1'] >= 0.)
    assert np.all(vdf['Tax_ST_CG_RATE2'] >= 0.)
    assert np.all(vdf['Tax_ST_CG_APPRATE'] == 0.)
    assert np.allclose(vdf['Total_Tax_STCG'],
                       (vdf['Tax_ST_CG_RATE1'] +
                        vdf['Tax_ST_CG_RATE2'] +
                        vdf['Tax_ST_CG_APPRATE']))
    assert np.all(vdf['Tax_LT_CG_RATE1'] >= 0.)
    assert np.all(vdf['Tax_LT_CG_RATE2'] >= 0.)
    assert np.allclose(vdf['Total_Tax_LTCG'],
                       vdf['Tax_LT_CG_RATE1'] + vdf['Tax_LT_CG_RATE2'])
    assert np.allclose(vdf['Total_Tax_Cap_Gains'],
                       vdf['Total_Tax_STCG'] + vdf['Total_Tax_LTCG'])
    assert np.all(vdf['tax_Aggregate_Income'] >= 0.)
    assert np.all(vdf['tax_TI_special_rates'] >= 0.)
    assert np.all(vdf['rebate_agri'] == 0.)
    exp = vdf['tax_Aggregate_Income'] + vdf['tax_TI_special_rates']
    exp -= vdf['rebate_agri']
    assert np.allclose(vdf['tax_TTI'], exp)
    assert np.all(vdf['rebate'] >= 0.)
    assert np.all(vdf['surcharge'] >= 0.)
    assert np.all(vdf['cess'] >= 0.)
    assert np.all(vdf['pitax'] >= 0.)
    exp = vdf['tax_TTI'] - vdf['rebate'] + vdf['surcharge'] + vdf['cess']
    assert np.allclose(vdf['pitax'], exp)
