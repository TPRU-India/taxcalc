# CODING-STYLE CHECKS:
# pycodestyle test_records.py

import os
import json
import numpy as np
from numpy.testing import assert_array_equal
import pandas as pd
import pytest
from io import StringIO
from taxcalc import GrowFactors, Policy, GSTRecords, Calculator


def test_incorrect_Records_instantiation(gst_sample):
    with pytest.raises(ValueError):
        recs = GSTRecords(data=list())
    with pytest.raises(ValueError):
        recs = GSTRecords(data=gst_sample, gfactors=list())
    with pytest.raises(ValueError):
        recs = GSTRecords(data=gst_sample, gfactors=None, weights=list())
    with pytest.raises(ValueError):
        recs = GSTRecords(data=gst_sample, gfactors=None, weights=None,
                          start_year=list())


def test_correct_Records_instantiation(gst_sample):
    rec1 = GSTRecords(data=gst_sample)
    assert rec1
    assert rec1.current_year == rec1.data_year
    rec1.set_current_year(rec1.data_year + 1)
    wghts_path = os.path.join(GSTRecords.CUR_PATH,
                              GSTRecords.GST_WEIGHTS_FILENAME)
    wghts_df = pd.read_csv(wghts_path)
    rec2 = GSTRecords(data=gst_sample,
                      gfactors=GrowFactors(),
                      weights=wghts_df,
                      start_year=GSTRecords.GSTCSV_YEAR)
    assert rec2
    assert rec2.current_year == rec2.data_year


def test_increment_year(gst_sample):
    recs = GSTRecords(data=gst_sample)
    assert recs.current_year == recs.data_year
    recs.increment_year()
    assert recs.current_year == recs.data_year + 1


def test_for_duplicate_names():
    varnames = set()
    for varname in GSTRecords.USABLE_READ_VARS:
        assert varname not in varnames
        varnames.add(varname)
        assert varname not in GSTRecords.CALCULATED_VARS
    varnames = set()
    for varname in GSTRecords.CALCULATED_VARS:
        assert varname not in varnames
        varnames.add(varname)
        assert varname not in GSTRecords.USABLE_READ_VARS
    varnames = set()
    for varname in GSTRecords.INTEGER_READ_VARS:
        assert varname not in varnames
        varnames.add(varname)
        assert varname in GSTRecords.USABLE_READ_VARS


def test_records_variables_content(tests_path):
    """
    Check completeness and consistency of records_variables.json content.
    """
    # specify test information
    reqkeys = ['type', 'desc', 'form']
    first_year = Policy.JSON_START_YEAR
    last_form_year = 2017
    # read JSON variable file into a dictionary
    path = os.path.join(tests_path, '..', 'gstrecords_variables.json')
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
