# CODING-STYLE CHECKS:
# pycodestyle test_records.py

import os
import json
import numpy as np
from numpy.testing import assert_array_equal
import pandas as pd
import pytest
from io import StringIO
from taxcalc import GrowFactors, Policy, CorpRecords, Calculator


def test_incorrect_Records_instantiation(cit_crosssample):
    with pytest.raises(ValueError):
        recs = CorpRecords(data=list())
    with pytest.raises(ValueError):
        recs = CorpRecords(data=cit_crosssample, data_type='cross-section',
                           gfactors=list())
    with pytest.raises(ValueError):
        recs = CorpRecords(data=cit_crosssample, data_type='cross-section',
                           gfactors=None, weights=list())
    with pytest.raises(ValueError):
        recs = CorpRecords(data=cit_crosssample, data_type='cross-section',
                           gfactors=None, weights=None, start_year=list())
    with pytest.raises(ValueError):
        recs = CorpRecords(data=cit_crosssample, data_type='something wrong',
                           gfactors=list())


def test_correct_Records_instantiation(cit_crosssample, cit_panelsample):
    rec1 = CorpRecords(data=cit_crosssample)
    # TODO: Add some checks for records
    assert True
    rec1.set_current_year(rec1.data_year + 1)
    wghts_path = os.path.join(CorpRecords.CUR_PATH,
                              CorpRecords.CIT_WEIGHTS_FILENAME)
    wghts_df = pd.read_csv(wghts_path)
    rec2 = CorpRecords(data=cit_crosssample,
                       gfactors=GrowFactors(),
                       weights=wghts_df,
                       start_year=CorpRecords.CITCSV_YEAR)
    # TODO: Repeat checks for records
    assert True
    assert rec2.current_year == rec2.data_year
    # try for panel results
    rec3 = CorpRecords(cit_panelsample, data_type='panel')
    assert rec3.current_year == CorpRecords.CITCSV_YEAR


def test_increment_year(cit_crosssample, cit_panelsample):
    recs = CorpRecords(data=cit_crosssample)
    assert recs.current_year == recs.data_year
    recs.increment_year()
    assert recs.current_year == recs.data_year + 1
    recs2 = CorpRecords(data=cit_panelsample, data_type='panel')
    assert recs2.current_year == recs2.data_year
    recs2.increment_year()
    assert recs2.current_year == recs2.data_year + 1


def test_for_duplicate_names():
    varnames = set()
    for varname in CorpRecords.USABLE_READ_VARS:
        assert varname not in varnames
        varnames.add(varname)
        assert varname not in CorpRecords.CALCULATED_VARS
    varnames = set()
    for varname in CorpRecords.CALCULATED_VARS:
        assert varname not in varnames
        varnames.add(varname)
        assert varname not in CorpRecords.USABLE_READ_VARS
    varnames = set()
    for varname in CorpRecords.INTEGER_READ_VARS:
        assert varname not in varnames
        varnames.add(varname)
        assert varname in CorpRecords.USABLE_READ_VARS


def test_records_variables_content(tests_path):
    """
    Check completeness and consistency of records_variables.json content.
    """
    # specify test information
    reqkeys = ['type', 'desc', 'form']
    first_year = Policy.JSON_START_YEAR
    last_form_year = 2017
    # read JSON variable file into a dictionary
    path = os.path.join(tests_path, '..', 'corprecords_variables.json')
    vfile = open(path, 'r')
    allvars = json.load(vfile)
    vfile.close()
    assert isinstance(allvars, dict)
    # check elements in each variable dictionary
    for iotype in ['read', 'calc']:
        for vname in allvars[iotype]:
            variable = allvars[iotype][vname]
            assert isinstance(variable, dict)
            # check that variable contains required keys
            for key in reqkeys:
                assert key in variable
            # check that required is true if it is present
            if 'required' in variable:
                assert variable['required'] is True
            # check that forminfo is dictionary with sensible years
            forminfo = variable['form']
            assert isinstance(forminfo, dict)
            for year_str in sorted(forminfo.keys()):
                year = int(year_str)
                assert year >= first_year
                assert year <= last_form_year
