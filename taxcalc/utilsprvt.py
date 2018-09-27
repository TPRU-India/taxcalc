"""
PRIVATE utility functions for Tax-Calculator PUBLIC utility functions.
"""
# CODING-STYLE CHECKS:
# pycodestyle utilsprvt.py
# pylint --disable=locally-disabled utilsprvt.py


EPSILON = 1e-9


def weighted_count_lt_zero(pdf, col_name, tolerance=-0.001):
    """
    Return weighted count of negative Pandas DataFrame col_name items.
    If condition is not met by any items, the result of applying sum to an
    empty dataframe is NaN.  This is undesirable and 0 is returned instead.
    """
    return pdf[pdf[col_name] < tolerance]['weight'].sum()


def weighted_count_gt_zero(pdf, col_name, tolerance=0.001):
    """
    Return weighted count of positive Pandas DataFrame col_name items.
    If condition is not met by any items, the result of applying sum to an
    empty dataframe is NaN.  This is undesirable and 0 is returned instead.
    """
    return pdf[pdf[col_name] > tolerance]['weight'].sum()


def weighted_count(pdf):
    """
    Return weighted count of items in Pandas DataFrame.
    """
    return pdf['weight'].sum()
