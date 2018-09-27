"""
PUBLIC low-level utility functions for Tax-Calculator.
"""
# CODING-STYLE CHECKS:
# pycodestyle utils.py
# pylint --disable=locally-disabled utils.py
#
# pylint: disable=too-many-lines

import os
import json
import collections
import pkg_resources
import numpy as np
import pandas as pd
from taxcalc.utilsprvt import (weighted_count_lt_zero,
                               weighted_count_gt_zero,
                               weighted_count)


# Items in the DIST_TABLE_COLUMNS list below correspond to the items in the
# DIST_TABLE_LABELS list below; this correspondence allows us to use this
# labels list to map a label to the correct column in a distribution table.

DIST_VARIABLES = ['expanded_income', 'c00100', 'aftertax_income', 'standard',
                  'c04470', 'c04600', 'c04800', 'taxbc', 'c62100', 'c09600',
                  'c05800', 'othertaxes', 'refund', 'c07100',
                  'iitax', 'payrolltax', 'combined', 'weight', 'ubi',
                  'benefit_cost_total', 'benefit_value_total']

DIST_TABLE_COLUMNS = ['weight',
                      'c00100',
                      'num_returns_StandardDed',
                      'standard',
                      'num_returns_ItemDed',
                      'c04470',
                      'c04600',
                      'c04800',
                      'taxbc',
                      'c62100',
                      'num_returns_AMT',
                      'c09600',
                      'c05800',
                      'c07100',
                      'othertaxes',
                      'refund',
                      'iitax',
                      'payrolltax',
                      'combined',
                      'ubi',
                      'benefit_cost_total',
                      'benefit_value_total',
                      'expanded_income',
                      'aftertax_income']

DIST_TABLE_LABELS = ['Returns',
                     'AGI',
                     'Standard Deduction Filers',
                     'Standard Deduction',
                     'Itemizers',
                     'Itemized Deduction',
                     'Personal Exemption',
                     'Taxable Income',
                     'Regular Tax',
                     'AMTI',
                     'AMT Filers',
                     'AMT',
                     'Tax before Credits',
                     'Non-refundable Credits',
                     'Other Taxes',
                     'Refundable Credits',
                     'Individual Income Tax Liabilities',
                     'Payroll Tax Liablities',
                     'Combined Payroll and Individual Income Tax Liabilities',
                     'Universal Basic Income',
                     'Total Cost of Benefits',
                     'Consumption Value of Benefits',
                     'Expanded Income',
                     'After-Tax Expanded Income']

# Items in the DIFF_TABLE_COLUMNS list below correspond to the items in the
# DIFF_TABLE_LABELS list below; this correspondence allows us to use this
# labels list to map a label to the correct column in a difference table.

DIFF_VARIABLES = ['expanded_income', 'c00100', 'aftertax_income',
                  'iitax', 'payrolltax', 'combined', 'weight', 'ubi',
                  'benefit_cost_total', 'benefit_value_total']

DIFF_TABLE_COLUMNS = ['count',
                      'tax_cut',
                      'perc_cut',
                      'tax_inc',
                      'perc_inc',
                      'mean',
                      'tot_change',
                      'share_of_change',
                      'ubi',
                      'benefit_cost_total',
                      'benefit_value_total',
                      'pc_aftertaxinc']

DIFF_TABLE_LABELS = ['All Tax Units',
                     'Tax Units with Tax Cut',
                     'Percent with Tax Cut',
                     'Tax Units with Tax Increase',
                     'Percent with Tax Increase',
                     'Average Tax Change',
                     'Total Tax Difference',
                     'Share of Overall Change',
                     'Universal Basic Income',
                     'Total Cost of Benefits',
                     'Consumption Value of Benefits',
                     '% Change in After-Tax Income']

DECILE_ROW_NAMES = ['0-10n', '0-10z', '0-10p',
                    '10-20', '20-30', '30-40', '40-50',
                    '50-60', '60-70', '70-80', '80-90', '90-100',
                    'ALL',
                    '90-95', '95-99', 'Top 1%']

STANDARD_ROW_NAMES = ['<$0K', '=$0K', '$0-10K', '$10-20K', '$20-30K',
                      '$30-40K', '$40-50K', '$50-75K', '$75-100K',
                      '$100-200K', '$200-500K', '$500-1000K', '>$1000K', 'ALL']

STANDARD_INCOME_BINS = [-9e99, -1e-9, 1e-9, 10e3, 20e3, 30e3, 40e3, 50e3,
                        75e3, 100e3, 200e3, 500e3, 1e6, 9e99]

SOI_AGI_BINS = [-9e99, 1.0, 5e3, 10e3, 15e3, 20e3, 25e3, 30e3, 40e3, 50e3,
                75e3, 100e3, 200e3, 500e3, 1e6, 1.5e6, 2e6, 5e6, 10e6, 9e99]


def unweighted_sum(pdf, col_name):
    """
    Return unweighted sum of Pandas DataFrame col_name items.
    """
    return pdf[col_name].sum()


def weighted_sum(pdf, col_name):
    """
    Return weighted sum of Pandas DataFrame col_name items.
    """
    return (pdf[col_name] * pdf['weight']).sum()


def add_quantile_table_row_variable(pdf, income_measure, num_quantiles,
                                    decile_details=False,
                                    weight_by_income_measure=False):
    """
    Add a variable to specified Pandas DataFrame, pdf, that specifies the
    table row and is called 'table_row'.  The rows hold equal number of
    filing units when weight_by_income_measure=False or equal number of
    income dollars when weight_by_income_measure=True.  Assumes that
    specified pdf contains columns for the specified income_measure and
    for sample weights, weight.  When num_quantiles is 10 and decile_details
    is True, the bottom decile is broken up into three subgroups (neg, zero,
    and pos income_measure ) and the top decile is broken into three subgroups
    (90-95, 95-99, and top 1%).
    """
    assert isinstance(pdf, pd.DataFrame)
    assert income_measure in pdf
    if decile_details and num_quantiles != 10:
        msg = 'decile_details is True when num_quantiles is {}'
        raise ValueError(msg.format(num_quantiles))
    pdf.sort_values(by=income_measure, inplace=True)
    if weight_by_income_measure:
        pdf['cumsum_temp'] = np.cumsum(np.multiply(pdf[income_measure].values,
                                                   pdf['weight'].values))
        min_cumsum = pdf['cumsum_temp'].values[0]
    else:
        pdf['cumsum_temp'] = np.cumsum(pdf['weight'].values)
        min_cumsum = 0.  # because weight values are non-negative
    max_cumsum = pdf['cumsum_temp'].values[-1]
    cumsum_range = max_cumsum - min_cumsum
    bin_width = cumsum_range / float(num_quantiles)
    bin_edges = list(min_cumsum +
                     np.arange(0, (num_quantiles + 1)) * bin_width)
    bin_edges[-1] = 9e99  # raise top of last bin to include all observations
    bin_edges[0] = -9e99  # lower bottom of 1st bin to include all observations
    num_bins = num_quantiles
    if decile_details:
        assert bin_edges[1] > 1e-9  # bin_edges[1] is top of bottom decile
        bin_edges.insert(1, 1e-9)  # top of zeros
        bin_edges.insert(1, -1e-9)  # top of negatives
        bin_edges.insert(-1, bin_edges[-2] + 0.5 * bin_width)  # top of 90-95
        bin_edges.insert(-1, bin_edges[-2] + 0.4 * bin_width)  # top of 95-99
        num_bins += 4
    labels = range(1, (num_bins + 1))
    pdf['table_row'] = pd.cut(pdf['cumsum_temp'], bin_edges,
                              right=False, labels=labels)
    pdf.drop('cumsum_temp', axis=1, inplace=True)
    return pdf


def add_income_table_row_variable(pdf, income_measure, bin_edges):
    """
    Add a variable to specified Pandas DataFrame, pdf, that specifies the
    table row and is called 'table_row'.  The rows are defined by the
    specified bin_edges function argument.  Note that the bin groupings
    are LEFT INCLUSIVE, which means that bin_edges=[1,2,3,4] implies these
    three bin groupings: [1,2), [2,3), [3,4).

    Parameters
    ----------
    pdf: Pandas DataFrame
        the object to which we are adding bins

    income_measure: String
        specifies income variable used to construct bins

    bin_edges: list of scalar bin edges

    Returns
    -------
    pdf: Pandas DataFrame
        the original input plus the added 'table_row' column
    """
    assert isinstance(pdf, pd.DataFrame)
    assert income_measure in pdf
    assert isinstance(bin_edges, list)
    pdf['table_row'] = pd.cut(pdf[income_measure], bin_edges, right=False)
    return pdf


def get_sums(pdf):
    """
    Compute unweighted sum of items in each column of Pandas DataFrame, pdf.

    Returns
    -------
    Pandas Series object containing column sums indexed by pdf column names.
    """
    sums = dict()
    for col in pdf.columns.values.tolist():
        if col != 'table_row':
            sums[col] = pdf[col].sum()
    return pd.Series(sums, name='ALL')


def create_distribution_table(vdf, groupby, income_measure):
    """
    Get results from vdf, sort them by expanded_income based on groupby,
    and return them as a table.

    Parameters
    ----------
    vdf : Pandas DataFrame including columns named in DIST_TABLE_COLUMNS list
        for example, an object returned from the Calculator class
        distribution_table_dataframe method

    groupby : String object
        options for input: 'weighted_deciles' or
                           'standard_income_bins' or 'soi_agi_bins'
        determines how the rows in the resulting Pandas DataFrame are sorted

    income_measure: String object
        options for input: 'expanded_income' or 'expanded_income_baseline'
        determines which variable is used to sort rows

    Returns
    -------
    distribution table as a Pandas DataFrame with DIST_TABLE_COLUMNS and
    groupby rows.
    NOTE: when groupby is 'weighted_deciles', the returned table has three
          extra rows containing top-decile detail consisting of statistics
          for the 0.90-0.95 quantile range (bottom half of top decile),
          for the 0.95-0.99 quantile range, and
          for the 0.99-1.00 quantile range (top one percent); and the
          returned table splits the bottom decile into filing units with
          negative (denoted by a 0-10n row label),
          zero (denoted by a 0-10z row label), and
          positive (denoted by a 0-10p row label) values of the
          specified income_measure.
    """
    # pylint: disable=too-many-statements,too-many-branches
    # nested function that returns calculated column statistics as a DataFrame
    def stat_dataframe(gpdf):
        """
        Returns calculated distribution table column statistics derived from
        the specified grouped Dataframe object, gpdf.
        """
        unweighted_columns = ['weight', 'num_returns_StandardDed',
                              'num_returns_ItemDed', 'num_returns_AMT']
        sdf = pd.DataFrame()
        for col in DIST_TABLE_COLUMNS:
            if col in unweighted_columns:
                sdf[col] = gpdf.apply(unweighted_sum, col)
            else:
                sdf[col] = gpdf.apply(weighted_sum, col)
        return sdf
    # main logic of create_distribution_table
    assert isinstance(vdf, pd.DataFrame)
    assert (groupby == 'weighted_deciles' or
            groupby == 'standard_income_bins' or
            groupby == 'soi_agi_bins')
    assert (income_measure == 'expanded_income' or
            income_measure == 'expanded_income_baseline')
    assert income_measure in vdf
    assert 'table_row' not in list(vdf.columns.values)
    # sort the data given specified groupby and income_measure
    if groupby == 'weighted_deciles':
        pdf = add_quantile_table_row_variable(vdf, income_measure,
                                              10, decile_details=True)
    elif groupby == 'standard_income_bins':
        pdf = add_income_table_row_variable(vdf, income_measure,
                                            STANDARD_INCOME_BINS)
    elif groupby == 'soi_agi_bins':
        pdf = add_income_table_row_variable(vdf, income_measure,
                                            SOI_AGI_BINS)
    # construct grouped DataFrame
    gpdf = pdf.groupby('table_row', as_index=False)
    dist_table = stat_dataframe(gpdf)
    del pdf['table_row']
    # compute sum row
    sum_row = get_sums(dist_table)[dist_table.columns]
    # handle placement of sum_row in table
    if groupby == 'weighted_deciles':
        # compute top-decile row
        lenindex = len(dist_table.index)
        assert lenindex == 14  # rows should be indexed from 0 to 13
        topdec_row = get_sums(dist_table[11:lenindex])[dist_table.columns]
        # move top-decile detail rows to make room for topdec_row and sum_row
        dist_table = dist_table.reindex(index=range(0, lenindex + 2))
        # pylint: disable=no-member
        dist_table.iloc[15] = dist_table.iloc[13]
        dist_table.iloc[14] = dist_table.iloc[12]
        dist_table.iloc[13] = dist_table.iloc[11]
        dist_table.iloc[12] = sum_row
        dist_table.iloc[11] = topdec_row
        del topdec_row
    else:
        dist_table = dist_table.append(sum_row)
    del sum_row
    # set print display format for float table elements
    pd.options.display.float_format = '{:8,.0f}'.format
    # ensure dist_table columns are in correct order
    assert dist_table.columns.values.tolist() == DIST_TABLE_COLUMNS
    # add row names to table if using weighted_deciles or standard_income_bins
    if groupby == 'weighted_deciles':
        rownames = DECILE_ROW_NAMES
    elif groupby == 'standard_income_bins':
        rownames = STANDARD_ROW_NAMES
    else:
        rownames = None
    if rownames:
        assert len(dist_table.index) == len(rownames)
        dist_table.index = rownames
        del rownames
    # delete intermediate Pandas DataFrame objects
    del gpdf
    del pdf
    # return table as Pandas DataFrame
    vdf.sort_index(inplace=True)
    return dist_table


def create_difference_table(vdf1, vdf2, groupby, tax_to_diff):
    """
    Get results from two different vdf, construct tax difference results,
    and return the difference statistics as a table.

    Parameters
    ----------
    vdf1 : Pandas DataFrame including columns named in DIFF_VARIABLES list
           for example, object returned from a dataframe(DIFF_VARIABLE) call
           on the basesline Calculator object

    vdf2 : Pandas DataFrame including columns in the DIFF_VARIABLES list
           for example, object returned from a dataframe(DIFF_VARIABLE) call
           on the reform Calculator object

    groupby : String object
        options for input: 'weighted_deciles' or
                           'standard_income_bins' or 'soi_agi_bins'
        determines how the rows in the resulting Pandas DataFrame are sorted

    tax_to_diff : String object
        options for input: 'iitax', 'payrolltax', 'combined'
        specifies which tax to difference

    Returns
    -------
    difference table as a Pandas DataFrame with DIFF_TABLE_COLUMNS and
    groupby rows.
    NOTE: when groupby is 'weighted_deciles', the returned table has three
          extra rows containing top-decile detail consisting of statistics
          for the 0.90-0.95 quantile range (bottom half of top decile),
          for the 0.95-0.99 quantile range, and
          for the 0.99-1.00 quantile range (top one percent); and the
          returned table splits the bottom decile into filing units with
          negative (denoted by a 0-10n row label),
          zero (denoted by a 0-10z row label), and
          positive (denoted by a 0-10p row label) values of the
          specified income_measure.
    """
    # pylint: disable=too-many-statements,too-many-locals
    # nested function that creates dataframe containing additive statistics
    def additive_stats_dataframe(gpdf):
        """
        Nested function that returns additive stats DataFrame derived from gpdf
        """
        sdf = pd.DataFrame()
        sdf['count'] = gpdf.apply(weighted_count)
        sdf['tax_cut'] = gpdf.apply(weighted_count_lt_zero, 'tax_diff')
        sdf['tax_inc'] = gpdf.apply(weighted_count_gt_zero, 'tax_diff')
        sdf['tot_change'] = gpdf.apply(weighted_sum, 'tax_diff')
        sdf['ubi'] = gpdf.apply(weighted_sum, 'ubi')
        sdf['benefit_cost_total'] = gpdf.apply(weighted_sum,
                                               'benefit_cost_total')
        sdf['benefit_value_total'] = gpdf.apply(weighted_sum,
                                                'benefit_value_total')
        sdf['atinc1'] = gpdf.apply(weighted_sum, 'atinc1')
        sdf['atinc2'] = gpdf.apply(weighted_sum, 'atinc2')
        return sdf
    # main logic of create_difference_table
    assert isinstance(vdf1, pd.DataFrame)
    assert isinstance(vdf2, pd.DataFrame)
    assert np.allclose(vdf1['weight'], vdf2['weight'])  # rows in same order
    assert (groupby == 'weighted_deciles' or
            groupby == 'standard_income_bins' or
            groupby == 'soi_agi_bins')
    assert 'expanded_income' in vdf1
    assert (tax_to_diff == 'iitax' or
            tax_to_diff == 'payrolltax' or
            tax_to_diff == 'combined')
    assert 'table_row' not in list(vdf1.columns.values)
    assert 'table_row' not in list(vdf2.columns.values)
    baseline_expanded_income = 'expanded_income_baseline'
    vdf2[baseline_expanded_income] = vdf1['expanded_income']
    vdf2['tax_diff'] = vdf2[tax_to_diff] - vdf1[tax_to_diff]
    vdf2['atinc1'] = vdf1['aftertax_income']
    vdf2['atinc2'] = vdf2['aftertax_income']
    # add table_row column to vdf2 given specified groupby and income_measure
    if groupby == 'weighted_deciles':
        pdf = add_quantile_table_row_variable(vdf2, baseline_expanded_income,
                                              10, decile_details=True)
    elif groupby == 'standard_income_bins':
        pdf = add_income_table_row_variable(vdf2, baseline_expanded_income,
                                            STANDARD_INCOME_BINS)
    elif groupby == 'soi_agi_bins':
        pdf = add_income_table_row_variable(vdf2, baseline_expanded_income,
                                            SOI_AGI_BINS)
    # create grouped Pandas DataFrame
    gpdf = pdf.groupby('table_row', as_index=False)
    del pdf['table_row']
    # create additive difference table statistics from gpdf
    diff_table = additive_stats_dataframe(gpdf)
    # calculate additive statistics on sums row
    sum_row = get_sums(diff_table)[diff_table.columns]
    # handle placement of sum_row in table
    if groupby == 'weighted_deciles':
        # compute top-decile row
        lenindex = len(diff_table.index)
        assert lenindex == 14  # rows should be indexed from 0 to 13
        topdec_row = get_sums(diff_table[11:lenindex])[diff_table.columns]
        # move top-decile detail rows to make room for topdec_row and sum_row
        diff_table = diff_table.reindex(index=range(0, lenindex + 2))
        # pylint: disable=no-member
        diff_table.iloc[15] = diff_table.iloc[13]
        diff_table.iloc[14] = diff_table.iloc[12]
        diff_table.iloc[13] = diff_table.iloc[11]
        diff_table.iloc[12] = sum_row
        diff_table.iloc[11] = topdec_row
        del topdec_row
    else:
        diff_table = diff_table.append(sum_row)
    # delete intermediate Pandas DataFrame objects
    del gpdf
    del pdf
    # compute non-additive stats in each table cell
    count = diff_table['count']
    diff_table['perc_cut'] = np.where(count > 0.,
                                      100 * diff_table['tax_cut'] / count,
                                      0.)
    diff_table['perc_inc'] = np.where(count > 0.,
                                      100 * diff_table['tax_inc'] / count,
                                      0.)
    diff_table['mean'] = np.where(count > 0.,
                                  diff_table['tot_change'] / count,
                                  0.)
    total_change = sum_row['tot_change']
    diff_table['share_of_change'] = np.where(total_change == 0.,
                                             np.nan,
                                             (100 * diff_table['tot_change'] /
                                              total_change))
    diff_table['pc_aftertaxinc'] = np.where(diff_table['atinc1'] == 0.,
                                            np.nan,
                                            (100 * (diff_table['atinc2'] /
                                                    diff_table['atinc1'] - 1)))
    # delete intermediate Pandas DataFrame objects
    del diff_table['atinc1']
    del diff_table['atinc2']
    del count
    del sum_row
    # set print display format for float table elements
    pd.options.display.float_format = '{:10,.2f}'.format
    # put diff_table columns in correct order
    diff_table = diff_table.reindex(columns=DIFF_TABLE_COLUMNS)
    # add row names to table if using weighted_deciles or standard_income_bins
    if groupby == 'weighted_deciles':
        rownames = DECILE_ROW_NAMES
    elif groupby == 'standard_income_bins':
        rownames = STANDARD_ROW_NAMES
    else:
        rownames = None
    if rownames:
        assert len(diff_table.index) == len(rownames)
        diff_table.index = rownames
        del rownames
    # return table as Pandas DataFrame
    vdf1.sort_index(inplace=True)
    vdf2.sort_index(inplace=True)
    return diff_table


def create_diagnostic_table(vdf, year):
    """
    Extract single-year diagnostic table from Pandas DataFrame object
    derived from a Calculator object using the dataframe(DIST_VARIABLES)
    method.

    Parameters
    ----------
    vdf : Pandas DataFrame object containing the variables

    year : assessment year for which variables are drawn from Calculator object

    Returns
    -------
    Pandas DataFrame object containing the diagnostic table
    """
    # pylint: disable=too-many-statements
    def diagnostic_table_odict(recs):
        """
        Nested function that extracts diagnostic table dictionary from
        the specified Pandas DataFrame object, vdf.

        Parameters
        ----------
        vdf : Pandas DataFrame object containing the variables

        Returns
        -------
        ordered dictionary of variable names and aggregate weighted values
        """
        # aggregate weighted values expressed in millions or billions
        in_millions = 1.0e-6
        in_billions = 1.0e-9
        odict = collections.OrderedDict()
        # total number of filing units
        wghts = vdf['weight']
        odict['Returns (#m)'] = wghts.sum() * in_millions
        # adjusted gross income
        agi = vdf['c00100']
        odict['AGI ($b)'] = (agi * wghts).sum() * in_billions
        # number of itemizers
        num = (wghts[vdf['c04470'] > 0.].sum())
        odict['Itemizers (#m)'] = num * in_millions
        # itemized deduction
        ided1 = vdf['c04470'] * wghts
        val = ided1[vdf['c04470'] > 0.].sum()
        odict['Itemized Deduction ($b)'] = val * in_billions
        # number of standard deductions
        num = wghts[vdf['standard'] > 0.].sum()
        odict['Standard Deduction Filers (#m)'] = num * in_millions
        # standard deduction
        sded1 = recs.standard * wghts
        val = sded1[vdf['standard'] > 0.].sum()
        odict['Standard Deduction ($b)'] = val * in_billions
        # personal exemption
        val = (vdf['c04600'] * wghts).sum()
        odict['Personal Exemption ($b)'] = val * in_billions
        # taxable income
        val = (vdf['c04800'] * wghts).sum()
        odict['Taxable Income ($b)'] = val * in_billions
        # regular tax liability
        val = (vdf['taxbc'] * wghts).sum()
        odict['Regular Tax ($b)'] = val * in_billions
        # AMT taxable income
        odict['AMT Income ($b)'] = ((vdf['c62100'] * wghts).sum() *
                                    in_billions)
        # total AMT liability
        odict['AMT Liability ($b)'] = ((vdf['c09600'] * wghts).sum() *
                                       in_billions)
        # number of people paying AMT
        odict['AMT Filers (#m)'] = (wghts[vdf['c09600'] > 0.].sum() *
                                    in_millions)
        # tax before credits
        val = (vdf['c05800'] * wghts).sum()
        odict['Tax before Credits ($b)'] = val * in_billions
        # refundable credits
        val = (vdf['refund'] * wghts).sum()
        odict['Refundable Credits ($b)'] = val * in_billions
        # nonrefundable credits
        val = (vdf['c07100'] * wghts).sum()
        odict['Nonrefundable Credits ($b)'] = val * in_billions
        # reform surtaxes (part of federal individual income tax liability)
        val = (vdf['surtax'] * wghts).sum()
        odict['Reform Surtaxes ($b)'] = val * in_billions
        # other taxes on Form 1040
        val = (vdf['othertaxes'] * wghts).sum()
        odict['Other Taxes ($b)'] = val * in_billions
        # federal individual income tax liability
        val = (vdf['iitax'] * wghts).sum()
        odict['Ind Income Tax ($b)'] = val * in_billions
        # OASDI+HI payroll tax liability (including employer share)
        val = (vdf['payrolltax'] * wghts).sum()
        odict['Payroll Taxes ($b)'] = val * in_billions
        # combined income and payroll tax liability
        val = (vdf['combined'] * wghts).sum()
        odict['Combined Liability ($b)'] = val * in_billions
        # number of tax units with non-positive income tax liability
        num = (wghts[vdf['iitax'] <= 0]).sum()
        odict['With Income Tax <= 0 (#m)'] = num * in_millions
        # number of tax units with non-positive combined tax liability
        num = (wghts[vdf['combined'] <= 0]).sum()
        odict['With Combined Tax <= 0 (#m)'] = num * in_millions
        return odict
    # tabulate diagnostic table
    odict = diagnostic_table_odict(vdf)
    pdf = pd.DataFrame(data=odict, index=[year], columns=odict.keys())
    pdf = pdf.transpose()
    pd.options.display.float_format = '{:8,.1f}'.format
    del odict
    return pdf


def read_egg_csv(fname, index_col=None):
    """
    Read from egg the file named fname that contains CSV data and
    return pandas DataFrame containing the data.
    """
    try:
        path_in_egg = os.path.join('taxcalc', fname)
        vdf = pd.read_csv(
            pkg_resources.resource_stream(
                pkg_resources.Requirement.parse('taxcalc'),
                path_in_egg),
            index_col=index_col
        )
    except Exception:
        raise ValueError('could not read {} data from egg'.format(fname))
    # cannot call read_egg_ function in unit tests
    return vdf  # pragma: no cover


def read_egg_json(fname):
    """
    Read from egg the file named fname that contains JSON data and
    return dictionary containing the data.
    """
    try:
        path_in_egg = os.path.join('taxcalc', fname)
        pdict = json.loads(
            pkg_resources.resource_stream(
                pkg_resources.Requirement.parse('taxcalc'),
                path_in_egg).read().decode('utf-8'),
            object_pairs_hook=collections.OrderedDict
        )
    except Exception:
        raise ValueError('could not read {} data from egg'.format(fname))
    # cannot call read_egg_ function in unit tests
    return pdict  # pragma: no cover


def bootstrap_se_ci(data, seed, num_samples, statistic, alpha):
    """
    Return bootstrap estimate of standard error of statistic and
    bootstrap estimate of 100*(1-2*alpha)% confidence interval for statistic
    in a dictionary along with specified seed and nun_samples (B) and alpha.
    """
    assert isinstance(data, np.ndarray)
    assert isinstance(seed, int)
    assert isinstance(num_samples, int)
    assert callable(statistic)  # function that computes statistic from data
    assert isinstance(alpha, float)
    bsest = dict()
    bsest['seed'] = seed
    np.random.seed(seed)  # pylint: disable=no-member
    dlen = len(data)
    idx = np.random.randint(low=0, high=dlen,   # pylint: disable=no-member
                            size=(num_samples, dlen))
    samples = data[idx]
    stat = statistic(samples, axis=1)
    bsest['B'] = num_samples
    bsest['se'] = np.std(stat, ddof=1)
    stat = np.sort(stat)
    bsest['alpha'] = alpha
    bsest['cilo'] = stat[int(round(alpha * num_samples)) - 1]
    bsest['cihi'] = stat[int(round((1 - alpha) * num_samples)) - 1]
    return bsest


def nonsmall_diffs(linelist1, linelist2, small=0.0):
    """
    Return True if line lists differ significantly; otherwise return False.
    Significant numerical difference means one or more numbers differ (between
    linelist1 and linelist2) by more than the specified small amount.
    """
    # embedded function used only in nonsmall_diffs function
    def isfloat(value):
        """
        Return True if value can be cast to float; otherwise return False.
        """
        try:
            float(value)
            return True
        except ValueError:
            return False
    # begin nonsmall_diffs logic
    assert isinstance(linelist1, list)
    assert isinstance(linelist2, list)
    if len(linelist1) != len(linelist2):
        return True
    assert small >= 0.0 and small <= 1.0
    epsilon = 1e-6
    smallamt = small + epsilon
    for line1, line2 in zip(linelist1, linelist2):
        if line1 == line2:
            continue
        else:
            tokens1 = line1.replace(',', '').split()
            tokens2 = line2.replace(',', '').split()
            for tok1, tok2 in zip(tokens1, tokens2):
                tok1_isfloat = isfloat(tok1)
                tok2_isfloat = isfloat(tok2)
                if tok1_isfloat and tok2_isfloat:
                    if abs(float(tok1) - float(tok2)) <= smallamt:
                        continue
                    else:
                        return True
                elif not tok1_isfloat and not tok2_isfloat:
                    if tok1 == tok2:
                        continue
                    else:
                        return True
                else:
                    return True
        return False


def quantity_response(quantity,
                      price_elasticity,
                      aftertax_price1,
                      aftertax_price2,
                      income_elasticity,
                      aftertax_income1,
                      aftertax_income2):
    """
    Calculate dollar change in quantity using a log-log response equation,
    which assumes that the proportional change in the quantity is equal to
    the sum of two terms:
    (1) the proportional change in the quanitity's marginal aftertax price
        times an assumed price elasticity, and
    (2) the proportional change in aftertax income
        times an assumed income elasticity.

    Parameters
    ----------
    quantity: numpy array
        pre-response quantity whose response is being calculated

    price_elasticity: float
        coefficient of the percentage change in aftertax price of
        the quantity in the log-log response equation

    aftertax_price1: numpy array
        marginal aftertax price of the quanitity under baseline policy
          Note that this function forces prices to be in [0.01, inf] range,
          but the caller of this function may want to constrain negative
          or very small prices to be somewhat larger in order to avoid extreme
          proportional changes in price.
          Note this is NOT an array of marginal tax rates (MTR), but rather
            usually 1-MTR (or in the case of quantities, like charitable
            giving, whose MTR values are non-positive, 1+MTR).

    aftertax_price2: numpy array
        marginal aftertax price of the quantity under reform policy
          Note that this function forces prices to be in [0.01, inf] range,
          but the caller of this function may want to constrain negative
          or very small prices to be somewhat larger in order to avoid extreme
          proportional changes in price.
          Note this is NOT an array of marginal tax rates (MTR), but rather
            usually 1-MTR (or in the case of quantities, like charitable
            giving, whose MTR values are non-positive, 1+MTR).

    income_elasticity: float
        coefficient of the percentage change in aftertax income in the
        log-log response equation

    aftertax_income1: numpy array
        aftertax income under baseline policy
          Note that this function forces income to be in [1, inf] range,
          but the caller of this function may want to constrain negative
          or small incomes to be somewhat larger in order to avoid extreme
          proportional changes in aftertax income.

    aftertax_income2: numpy array
        aftertax income under reform policy
          Note that this function forces income to be in [1, inf] range,
          but the caller of this function may want to constrain negative
          or small incomes to be somewhat larger in order to avoid extreme
          proportional changes in aftertax income.

    Returns
    -------
    response: numpy array
        dollar change in quantity calculated from log-log response equation
    """
    # pylint: disable=too-many-arguments
    # compute price term in log-log response equation
    if price_elasticity == 0.:
        pch_price = np.zeros(quantity.shape)
    else:
        atp1 = np.where(aftertax_price1 < 0.01, 0.01, aftertax_price1)
        atp2 = np.where(aftertax_price2 < 0.01, 0.01, aftertax_price2)
        pch_price = atp2 / atp1 - 1.
    # compute income term in log-log response equation
    if income_elasticity == 0.:
        pch_income = np.zeros(quantity.shape)
    else:
        ati1 = np.where(aftertax_income1 < 1.0, 1.0, aftertax_income1)
        ati2 = np.where(aftertax_income2 < 1.0, 1.0, aftertax_income2)
        pch_income = ati2 / ati1 - 1.
    # compute response
    pch_q = price_elasticity * pch_price + income_elasticity * pch_income
    response = pch_q * quantity
    return response
