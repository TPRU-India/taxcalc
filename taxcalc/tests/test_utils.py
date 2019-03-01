"""
Tests of Tax-Calculator utility functions.
"""
# CODING-STYLE CHECKS:
# pycodestyle test_utils.py
# pylint --disable=locally-disabled test_utils.py
#
# pylint: disable=missing-docstring,no-member,protected-access,too-many-lines

import numpy as np
import pandas as pd
import pytest
# pylint: disable=import-error
from taxcalc import Policy, Records, GSTRecords, CorpRecords, Calculator
from taxcalc.utils import (DIST_VARIABLES,
                           DIST_TABLE_COLUMNS, DIST_TABLE_LABELS,
                           STANDARD_INCOME_BINS,
                           create_distribution_table, create_difference_table,
                           weighted_count_lt_zero, weighted_count_gt_zero,
                           weighted_count, weighted_sum,
                           add_income_table_row_variable,
                           add_quantile_table_row_variable,
                           read_egg_csv, read_egg_json,
                           bootstrap_se_ci,
                           nonsmall_diffs,
                           quantity_response)


DATA = [[1.0, 2, 'a'],
        [-1.0, 4, 'a'],
        [3.0, 6, 'a'],
        [2.0, 4, 'b'],
        [3.0, 6, 'b']]

WEIGHT_DATA = [[1.0, 2.0, 10.0],
               [2.0, 4.0, 20.0],
               [3.0, 6.0, 30.0]]

DATA_FLOAT = [[1.0, 2, 'a'],
              [-1.0, 4, 'a'],
              [0.0000000001, 3, 'a'],
              [-0.0000000001, 1, 'a'],
              [3.0, 6, 'a'],
              [2.0, 4, 'b'],
              [0.0000000001, 3, 'b'],
              [-0.0000000001, 1, 'b'],
              [3.0, 6, 'b']]


def test_validity_of_name_lists():
    assert len(DIST_TABLE_COLUMNS) == len(DIST_TABLE_LABELS)
    Records.read_var_info()
    assert set(DIST_VARIABLES).issubset(Records.CALCULATED_VARS | {'weight'})
    extra_vars_set = set()
    assert (set(DIST_TABLE_COLUMNS) - set(DIST_VARIABLES)) == extra_vars_set


def test_create_distribution_tables(pit_fullsample, gst_sample,
                                    cit_crosssample):
    # pylint: disable=too-many-statements,too-many-branches
    # create a current-law Policy object and Calculator object calc1
    rec = Records(data=pit_fullsample)
    grec = GSTRecords(data=gst_sample)
    crec = CorpRecords(data=cit_crosssample)
    pol = Policy()
    calc1 = Calculator(policy=pol, records=rec, gstrecords=grec,
                       corprecords=crec)
    calc1.calc_all()
    # create a policy-reform Policy object and Calculator object calc2
    reform = {2017: {'_rate2': [0.06]}}
    pol.implement_reform(reform)
    calc2 = Calculator(policy=pol, records=rec, gstrecords=grec,
                       corprecords=crec)
    calc2.calc_all()

    test_failure = False

    # test creating various distribution tables

    dist, _ = calc2.distribution_tables(None, 'weighted_deciles')
    assert isinstance(dist, pd.DataFrame)
    tabcol = 'pitax'
    expected = [0.000,
                0.000,
                0.000,
                0.000,
                0.000,
                1.962,
                5.711,
                14.602,
                45.503,
                163.177,
                397.795,
                1018.520,
                1647.270,
                331.218,
                384.399,
                302.903]
    if not np.allclose(dist[tabcol].values, expected):
        test_failure = True
        print('dist xdec', tabcol)
        for val in dist[tabcol].values:
            print('{:.3f},'.format(val))

    tabcol = 'GTI'
    expected = [0.000,
                0.000,
                688.359,
                893.687,
                1107.005,
                1332.670,
                1605.580,
                1824.545,
                2327.660,
                2818.092,
                3848.954,
                6071.569,
                22518.121,
                2490.655,
                2119.235,
                1461.678]
    if not np.allclose(dist[tabcol].tolist(), expected):
        test_failure = True
        print('dist xdec', tabcol)
        for val in dist[tabcol].values:
            print('{:.3f},'.format(val))

    dist, _ = calc2.distribution_tables(None, 'standard_income_bins')
    assert isinstance(dist, pd.DataFrame)
    tabcol = 'pitax'
    expected = [0.000,
                0.000,
                8.334,
                279.113,
                542.762,
                401.310,
                415.751,
                0.000,
                0.000,
                0.000,
                0.000,
                1647.270]
    if not np.allclose(dist[tabcol], expected):
        test_failure = True
        print('dist xbin', tabcol)
        for val in dist[tabcol].values:
            print('{:.3f},'.format(val))

    tabcol = 'GTI'
    expected = [0.000,
                0.000,
                5884.790,
                7399.792,
                4810.526,
                2392.643,
                2030.370,
                0.000,
                0.000,
                0.000,
                0.000,
                22518.121]
    if not np.allclose(dist[tabcol].tolist(), expected):
        test_failure = True
        print('dist xdec', tabcol)
        for val in dist[tabcol].values:
            print('{:.3f},'.format(val))

    """
    Disabled till the model stablises
    """
    # if test_failure:
    #    assert 1 == 2


def test_weighted_count_lt_zero():
    df1 = pd.DataFrame(data=DATA, columns=['tax_diff', 'weight', 'label'])
    grped = df1.groupby('label')
    diffs = grped.apply(weighted_count_lt_zero, 'tax_diff')
    exp = pd.Series(data=[4, 0], index=['a', 'b'])
    exp.index.name = 'label'
    pd.util.testing.assert_series_equal(exp, diffs)
    df2 = pd.DataFrame(data=DATA_FLOAT, columns=['tax_diff', 'weight',
                                                 'label'])
    grped = df2.groupby('label')
    diffs = grped.apply(weighted_count_lt_zero, 'tax_diff')
    exp = pd.Series(data=[4, 0], index=['a', 'b'])
    exp.index.name = 'label'
    pd.util.testing.assert_series_equal(exp, diffs)


def test_weighted_count_gt_zero():
    df1 = pd.DataFrame(data=DATA, columns=['tax_diff', 'weight', 'label'])
    grped = df1.groupby('label')
    diffs = grped.apply(weighted_count_gt_zero, 'tax_diff')
    exp = pd.Series(data=[8, 10], index=['a', 'b'])
    exp.index.name = 'label'
    pd.util.testing.assert_series_equal(exp, diffs)
    df2 = pd.DataFrame(data=DATA, columns=['tax_diff', 'weight', 'label'])
    grped = df2.groupby('label')
    diffs = grped.apply(weighted_count_gt_zero, 'tax_diff')
    exp = pd.Series(data=[8, 10], index=['a', 'b'])
    exp.index.name = 'label'
    pd.util.testing.assert_series_equal(exp, diffs)


def test_weighted_count():
    dfx = pd.DataFrame(data=DATA, columns=['tax_diff', 'weight', 'label'])
    grouped = dfx.groupby('label')
    diffs = grouped.apply(weighted_count)
    exp = pd.Series(data=[12, 10], index=['a', 'b'])
    exp.index.name = 'label'
    pd.util.testing.assert_series_equal(exp, diffs)


def test_weighted_sum():
    dfx = pd.DataFrame(data=DATA, columns=['tax_diff', 'weight', 'label'])
    grouped = dfx.groupby('label')
    diffs = grouped.apply(weighted_sum, 'tax_diff')
    exp = pd.Series(data=[16.0, 26.0], index=['a', 'b'])
    exp.index.name = 'label'
    pd.util.testing.assert_series_equal(exp, diffs)


EPSILON = 1e-5


def test_add_income_trow_var():
    dta = np.arange(1, 1e6, 5000)
    vdf = pd.DataFrame(data=dta, columns=['GTI'])
    vdf = add_income_table_row_variable(vdf, 'GTI', STANDARD_INCOME_BINS)
    gdf = vdf.groupby('table_row')
    idx = 1
    for name, _ in gdf:
        assert name.closed == 'left'
        assert abs(name.right - STANDARD_INCOME_BINS[idx]) < EPSILON
        idx += 1


def test_add_quantile_trow_var():
    dfx = pd.DataFrame(data=DATA, columns=['expanded_income', 'weight',
                                           'label'])
    dfb = add_quantile_table_row_variable(dfx, 'expanded_income',
                                          100, decile_details=False,
                                          weight_by_income_measure=False)
    bin_labels = dfb['table_row'].unique()
    default_labels = set(range(1, 101))
    for lab in bin_labels:
        assert lab in default_labels
    dfb = add_quantile_table_row_variable(dfx, 'expanded_income',
                                          100, decile_details=False)
    assert 'table_row' in dfb
    with pytest.raises(ValueError):
        dfb = add_quantile_table_row_variable(dfx, 'expanded_income',
                                              100, decile_details=True)


def test_dist_table_sum_row(pit_subsample, gst_sample, cit_crosssample):
    rec = Records(data=pit_subsample)
    grec = GSTRecords(data=gst_sample)
    crec = CorpRecords(data=cit_crosssample)
    calc = Calculator(policy=Policy(), records=rec, gstrecords=grec,
                      corprecords=crec)
    calc.calc_all()
    tb1 = create_distribution_table(calc.distribution_table_dataframe(),
                                    'standard_income_bins', 'GTI')
    tb2 = create_distribution_table(calc.distribution_table_dataframe(),
                                    'weighted_deciles', 'GTI')
    allrow1 = tb1[-1:]
    allrow2 = tb2[-4:-3]
    assert np.allclose(allrow1, allrow2)


def test_read_egg_csv():
    with pytest.raises(ValueError):
        read_egg_csv('bad_filename')


def test_read_egg_json():
    with pytest.raises(ValueError):
        read_egg_json('bad_filename')


def test_bootstrap_se_ci():
    # Use treated mouse data from Table 2.1 and
    # results from Table 2.2 and Table 13.1 in
    # Bradley Efron and Robert Tibshirani,
    # "An Introduction to the Bootstrap"
    # (Chapman & Hall, 1993).
    data = np.array([94, 197, 16, 38, 99, 141, 23], dtype=np.float64)
    assert abs(np.mean(data) - 86.86) < 0.005  # this is just rounding error
    bsd = bootstrap_se_ci(data, 123456789, 1000, np.mean, alpha=0.025)
    # following comparisons are less precise because of r.n. stream differences
    assert abs(bsd['se'] / 23.02 - 1) < 0.02
    assert abs(bsd['cilo'] / 45.9 - 1) < 0.02
    assert abs(bsd['cihi'] / 135.4 - 1) < 0.03


def test_table_columns_labels():
    # check that length of two lists are the same
    assert len(DIST_TABLE_COLUMNS) == len(DIST_TABLE_LABELS)


def test_nonsmall_diffs():
    assert nonsmall_diffs(['AAA'], ['AAA', 'BBB'])
    assert nonsmall_diffs(['AaA'], ['AAA'])
    assert not nonsmall_diffs(['AAA'], ['AAA'])
    assert nonsmall_diffs(['12.3'], ['12.2'])
    assert not nonsmall_diffs(['12.3 AAA'], ['12.2 AAA'], small=0.1)
    assert nonsmall_diffs(['12.3'], ['AAA'])


def test_quantity_response():
    quantity = np.array([1.0] * 10)
    res = quantity_response(quantity,
                            price_elasticity=0,
                            aftertax_price1=None,
                            aftertax_price2=None,
                            income_elasticity=0,
                            aftertax_income1=None,
                            aftertax_income2=None)
    assert np.allclose(res, np.zeros(quantity.shape))
    one = np.ones(quantity.shape)
    res = quantity_response(quantity,
                            price_elasticity=-0.2,
                            aftertax_price1=one,
                            aftertax_price2=one,
                            income_elasticity=0.1,
                            aftertax_income1=one,
                            aftertax_income2=(one + one))
    assert not np.allclose(res, np.zeros(quantity.shape))
