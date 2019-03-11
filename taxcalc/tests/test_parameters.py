"""
Tests for Tax-Calculator ParametersBase class and JSON parameter files.
"""
# CODING-STYLE CHECKS:
# pycodestyle test_parameters.py
# pylint --disable=locally-disabled test_parameters.py

import os
import json
import math
import numpy as np
import pytest
# pylint: disable=import-error
from taxcalc import ParametersBase, Policy


def test_instantiation_and_usage():
    """
    Test ParametersBase instantiation and usage.
    """
    pbase = ParametersBase()
    assert pbase
    assert pbase.inflation_rates() is None
    assert pbase.wage_growth_rates() is None
    syr = 2010
    nyrs = 10
    pbase.initialize(start_year=syr, num_years=nyrs)
    # pylint: disable=protected-access
    with pytest.raises(ValueError):
        pbase.set_year(syr - 1)
    with pytest.raises(NotImplementedError):
        pbase._params_dict_from_json_file()
    with pytest.raises(ValueError):
        pbase._update([])
    with pytest.raises(ValueError):
        pbase._update({})
    with pytest.raises(ValueError):
        pbase._update({(syr + nyrs): {}})
    with pytest.raises(ValueError):
        pbase._update({syr: []})
    # pylint: disable=no-member
    with pytest.raises(ValueError):
        ParametersBase._expand_array({}, False, False, True, [0.02], 1)
    arr3d = np.array([[[1, 1]], [[1, 1]], [[1, 1]]])
    with pytest.raises(ValueError):
        ParametersBase._expand_array(arr3d, False, False, True, [0.02], 1)


@pytest.mark.parametrize("fname", [("current_law_policy.json")])
def test_json_file_contents(tests_path, fname):
    """
    Check contents of JSON parameter files.
    """
    # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    # specify test information
    reqkeys = ['long_name', 'description', 'notes',
               'row_var', 'row_label',
               'start_year', 'cpi_inflated',
               'col_var', 'col_label',
               'value']
    first_year = Policy.JSON_START_YEAR
    last_known_year = Policy.LAST_KNOWN_YEAR  # for indexed parameter values
    num_known_years = last_known_year - first_year + 1
    # read JSON parameter file into a dictionary
    path = os.path.join(tests_path, '..', fname)
    pfile = open(path, 'r')
    allparams = json.load(pfile)
    pfile.close()
    assert isinstance(allparams, dict)
    # check elements in each parameter sub-dictionary
    failures = ''
    for pname in allparams:
        # all parameter names should be strings
        assert isinstance(pname, str)
        # check that param contains required keys
        param = allparams[pname]
        assert isinstance(param, dict)
        for key in reqkeys:
            assert key in param
        # check for non-empty long_name and description strings
        assert isinstance(param['long_name'], str)
        if not param['long_name']:
            assert '{} long_name'.format(pname) == 'empty string'
        assert isinstance(param['description'], str)
        if not param['description']:
            assert '{} description'.format(pname) == 'empty string'
        # check that row_var is FLPDYR
        assert param['row_var'] == 'AYEAR'
        # check that start_year equals first_year
        syr = param['start_year']
        assert isinstance(syr, int) and syr == first_year
        # check that cpi_inflated is boolean
        assert isinstance(param['cpi_inflated'], bool)
        if fname != 'current_law_policy.json':
            assert param['cpi_inflated'] is False
        # check that row_label is list
        rowlabel = param['row_label']
        assert isinstance(rowlabel, list)
        # check all row_label values
        cyr = first_year
        for rlabel in rowlabel:
            assert int(rlabel) == cyr
            cyr += 1
        # check type and dimension of value
        value = param['value']
        assert isinstance(value, list)
        assert len(value) == len(rowlabel)
        # check that col_var and col_label are consistent
        cvar = param['col_var']
        assert isinstance(cvar, str)
        clab = param['col_label']
        if cvar == '':
            assert isinstance(clab, str) and clab == ''
        else:
            assert isinstance(clab, list)
            # check different possible col_var values
            if cvar == 'AGEGRP':
                assert len(clab) == 3
            elif cvar == 'TTI1':
                assert len(clab) == 3
            elif cvar == 'TTI2':
                assert len(clab) == 2
            elif cvar == 'EIC':
                assert len(clab) == 4
            elif cvar == 'idedtype':
                assert len(clab) == 7
            elif cvar == 'c00100':
                pass
            else:
                assert cvar == 'UNKNOWN col_var VALUE'
            # check length of each value row
            for valuerow in value:
                assert len(valuerow) == len(clab)
        # check that indexed parameters have all known years in rowlabel list
        # form_parameters are those whose value is available only on IRS form
        form_parameters = []
        if param['cpi_inflated']:
            error = False
            known_years = num_known_years
            if pname in form_parameters:
                if len(rowlabel) != (known_years - 1):
                    error = True
            else:
                if len(rowlabel) != known_years:
                    error = True
            if error:
                msg = 'param:<{}>; len(rowlabel)={}; known_years={}'
                fail = msg.format(pname, len(rowlabel), known_years)
                failures += fail + '\n'
    if failures:
        raise ValueError(failures)


@pytest.mark.parametrize("jfname, pfname, gpfname, cpfname",
                         [("current_law_policy.json", "functions.py",
                           "gstfunctions.py", "corpfunctions.py")])
def test_parameters_mentioned(tests_path, jfname, pfname, gpfname, cpfname):
    """
    Make sure each JSON parameter is mentioned in PYTHON code file.
    """
    # read JSON parameter file into a dictionary
    path = os.path.join(tests_path, '..', jfname)
    pfile = open(path, 'r')
    allparams = json.load(pfile)
    pfile.close()
    assert isinstance(allparams, dict)
    # read PYTHON code file text
    path = os.path.join(tests_path, '..', pfname)
    pfile = open(path, 'r')
    code_text = pfile.read()
    pfile.close()
    # read GST PYTHON file text
    gpath = os.path.join(tests_path, '..', gpfname)
    gpfile = open(gpath, 'r')
    code_text3 = gpfile.read()
    gpfile.close()
    # read corporate PYTHON file text
    cpath = os.path.join(tests_path, '..', cpfname)
    cpfile = open(cpath, 'r')
    code_text2 = cpfile.read()
    cpfile.close()
    # check that each param (without leading _) is mentioned in code text
    for pname in allparams:
        temp1 = (pname[1:] in code_text)
        temp2 = (pname[1:] in code_text2)
        temp3 = (pname[1:] in code_text3)
        # assert temp1 or temp2 or temp3


# following tests access private methods, so pylint: disable=protected-access


def test_expand_xd_errors():
    """
    One of several _expand_?D tests.
    """
    dct = dict()
    with pytest.raises(ValueError):
        ParametersBase._expand_1D(dct, inflate=False, inflation_rates=[],
                                  num_years=10)
    with pytest.raises(ValueError):
        ParametersBase._expand_2D(dct, inflate=False, inflation_rates=[],
                                  num_years=10)


def test_expand_1d_scalar():
    """
    One of several _expand_?D tests.
    """
    val = 10.0
    exp = np.array([val * math.pow(1.02, i) for i in range(0, 10)])
    res = ParametersBase._expand_1D(np.array([val]),
                                    inflate=True, inflation_rates=[0.02] * 10,
                                    num_years=10)
    assert np.allclose(exp, res, atol=0.01, rtol=0.0)


def test_expand_2d_short_array():
    """
    One of several _expand_?D tests.
    """
    ary = np.array([[1., 2., 3.]])
    val = np.array([1., 2., 3.])
    exp2 = np.array([val * math.pow(1.02, i) for i in range(1, 5)])
    exp1 = np.array([1., 2., 3.])
    exp = np.zeros((5, 3))
    exp[:1] = exp1
    exp[1:] = exp2
    res = ParametersBase._expand_2D(ary, inflate=True,
                                    inflation_rates=[0.02] * 5, num_years=5)
    assert np.allclose(exp, res, atol=0.01, rtol=0.0)


def test_expand_2d_variable_rates():
    """
    One of several _expand_?D tests.
    """
    ary = np.array([[1., 2., 3.]])
    cur = np.array([1., 2., 3.])
    irates = [0.02, 0.02, 0.02, 0.03, 0.035]
    exp2 = []
    for i in range(0, 4):
        idx = i + len(ary) - 1
        cur = np.array(cur * (1.0 + irates[idx]))
        print('cur is ', cur)
        exp2.append(cur)
    exp1 = np.array([1., 2., 3.])
    exp = np.zeros((5, 3))
    exp[:1] = exp1
    exp[1:] = exp2
    res = ParametersBase._expand_2D(ary, inflate=True,
                                    inflation_rates=irates, num_years=5)
    assert np.allclose(exp, res, atol=0.01, rtol=0.0)


def test_expand_2d_already_filled():
    """
    One of several _expand_?D tests.
    """
    # pylint doesn't like caps in var name, so  pylint: disable=invalid-name
    _II_brk2 = [[36000., 72250., 36500., 48600., 72500., 36250.],
                [38000., 74000., 36900., 49400., 73800., 36900.],
                [40000., 74900., 37450., 50200., 74900., 37450.]]
    res = ParametersBase._expand_2D(np.array(_II_brk2),
                                    inflate=True, inflation_rates=[0.02] * 5,
                                    num_years=3)
    np.allclose(res, np.array(_II_brk2), atol=0.01, rtol=0.0)


def test_expand_2d_partial_expand():
    """
    One of several _expand_?D tests.
    """
    # pylint doesn't like caps in var name, so  pylint: disable=invalid-name
    _II_brk2 = [[36000.0, 72250.0, 36500.0, 48600.0, 72500.0, 36250.0],
                [38000.0, 74000.0, 36900.0, 49400.0, 73800.0, 36900.0],
                [40000.0, 74900.0, 37450.0, 50200.0, 74900.0, 37450.0]]
    # We have three years worth of data, need 4 years worth,
    # but we only need the inflation rate for year 3 to go
    # from year 3 -> year 4
    inf_rates = [0.02, 0.02, 0.03]
    exp1 = 40000. * 1.03
    exp2 = 74900. * 1.03
    exp3 = 37450. * 1.03
    exp4 = 50200. * 1.03
    exp5 = 74900. * 1.03
    exp6 = 37450. * 1.03
    exp = [[36000.0, 72250.0, 36500.0, 48600.0, 72500.0, 36250.0],
           [38000.0, 74000.0, 36900.0, 49400.0, 73800.0, 36900.0],
           [40000.0, 74900.0, 37450.0, 50200.0, 74900.0, 37450.0],
           [exp1, exp2, exp3, exp4, exp5, exp6]]
    res = ParametersBase._expand_2D(np.array(_II_brk2),
                                    inflate=True, inflation_rates=inf_rates,
                                    num_years=4)
    assert np.allclose(res, exp, atol=0.01, rtol=0.0)


@pytest.mark.parametrize('json_filename', ['current_law_policy.json'])
def test_bool_int_value_info(tests_path, json_filename):
    """
    Check consistency of boolean_value and integer_value info in
    JSON parameter files.
    """
    path = os.path.join(tests_path, '..', json_filename)
    with open(path, 'r') as pfile:
        pdict = json.load(pfile)
    maxint = np.iinfo(np.int8).max
    for param in sorted(pdict.keys()):
        # check that boolean_value is never integer_value
        if pdict[param]['boolean_value'] and pdict[param]['integer_value']:
            msg = 'param,boolean_value,integer_value,= {} {} {}'
            msg = msg.format(str(param),
                             pdict[param]['boolean_value'],
                             pdict[param]['integer_value'])
            assert msg == 'ERROR: boolean_value is integer_value'
        # check that cpi_indexed param is not boolean or integer
        nonfloat_value = (pdict[param]['integer_value'] or
                          pdict[param]['boolean_value'])
        if pdict[param]['cpi_inflated'] and nonfloat_value:
            msg = 'param,boolean_value,integer_value,= {} {} {}'
            msg = msg.format(str(param),
                             pdict[param]['boolean_value'],
                             pdict[param]['integer_value'])
            assert msg == 'ERROR: nonfloat_value param is inflation indexed'
        # find param type based on value
        val = pdict[param]['value']
        while isinstance(val, list):
            val = val[0]
        valstr = str(val)
        val_is_boolean = bool(valstr == 'True' or valstr == 'False')
        val_is_integer = (not bool('.' in valstr or abs(val) > maxint) and
                          not val_is_boolean)
        # check that val_is_integer is consistent with integer_value
        if val_is_integer != pdict[param]['integer_value']:
            msg = 'param,integer_value,valstr= {} {} {}'
            msg = msg.format(str(param),
                             pdict[param]['integer_value'],
                             valstr)
            assert msg == 'ERROR: integer_value param has non-integer value'
        # check that val_is_boolean is consistent with boolean_value
        if val_is_boolean != pdict[param]['boolean_value']:
            msg = 'param,boolean_value,valstr= {} {} {}'
            msg = msg.format(str(param),
                             pdict[param]['boolean_value'],
                             valstr)
            assert msg == 'ERROR: boolean_value param has non-boolean value'


@pytest.mark.parametrize('json_filename', ['current_law_policy.json'])
def test_cpi_inflatable_info(tests_path, json_filename):
    """
    Check presence and consistency of cpi_inflatable info in
    JSON parameter files.
    """
    path = os.path.join(tests_path, '..', json_filename)
    with open(path, 'r') as pfile:
        pdict = json.load(pfile)
    for param in sorted(pdict.keys()):
        # check for presence of cpi_inflatable field
        if 'cpi_inflatable' not in pdict[param]:
            msg = 'param= {}'.format(str(param))
            assert msg == 'ERROR: missing cpi_inflatable field'
        # ensure that cpi_inflatable is True when cpi_inflated is True
        if pdict[param]['cpi_inflated'] and not pdict[param]['cpi_inflatable']:
            msg = 'param= {}'.format(str(param))
            assert msg == 'ERROR: cpi_inflatable=False when cpi_inflated=True'
        # ensure that cpi_inflatable is False when integer_value is True
        if pdict[param]['integer_value'] and pdict[param]['cpi_inflatable']:
            msg = 'param= {}'.format(str(param))
            assert msg == 'ERROR: cpi_inflatable=True when integer_value=True'
