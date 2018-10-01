# CODING-STYLE CHECKS:
# pycodestyle test_records.py

import os
import json
import numpy as np
from numpy.testing import assert_array_equal
import pandas as pd
import pytest
from io import StringIO
from taxcalc import GrowFactors, Policy, Records, Calculator


def test_incorrect_Records_instantiation(pit_subsample):
    with pytest.raises(ValueError):
        recs = Records(data=list())
    with pytest.raises(ValueError):
        recs = Records(data=pit_subsample, gfactors=list())
    with pytest.raises(ValueError):
        recs = Records(data=pit_subsample, gfactors=None, weights=list())
    with pytest.raises(ValueError):
        recs = Records(data=pit_subsample, gfactors=None, weights=None,
                       start_year=list())


def test_correct_Records_instantiation(pit_subsample):
    rec1 = Records(data=pit_subsample)
    assert rec1
    assert np.all(rec1.AGEGRP >= 0) and np.all(rec1.AGEGRP <= 2)
    assert rec1.current_year == rec1.data_year
    rec1.set_current_year(rec1.data_year + 1)
    wghts_path = os.path.join(Records.CUR_PATH, Records.PIT_WEIGHTS_FILENAME)
    wghts_df = pd.read_csv(wghts_path)
    rec2 = Records(data=pit_subsample,
                   gfactors=GrowFactors(),
                   weights=wghts_df,
                   start_year=Records.PITCSV_YEAR)
    assert rec2
    assert np.all(rec1.AGEGRP >= 0) and np.all(rec1.AGEGRP <= 2)
    assert rec2.current_year == rec2.data_year


def test_increment_year(pit_subsample):
    recs = Records(data=pit_subsample)
    assert recs.current_year == recs.data_year
    recs.increment_year()
    assert recs.current_year == recs.data_year + 1


def test_for_duplicate_names():
    varnames = set()
    for varname in Records.USABLE_READ_VARS:
        assert varname not in varnames
        varnames.add(varname)
        assert varname not in Records.CALCULATED_VARS
    varnames = set()
    for varname in Records.CALCULATED_VARS:
        assert varname not in varnames
        varnames.add(varname)
        assert varname not in Records.USABLE_READ_VARS
    varnames = set()
    for varname in Records.INTEGER_READ_VARS:
        assert varname not in varnames
        varnames.add(varname)
        assert varname in Records.USABLE_READ_VARS


def test_records_variables_content(tests_path):
    """
    Check completeness and consistency of records_variables.json content.
    """
    # specify test information
    reqkeys = ['type', 'desc', 'form']
    first_year = Policy.JSON_START_YEAR
    last_form_year = 2017
    # read JSON variable file into a dictionary
    path = os.path.join(tests_path, '..', 'records_variables.json')
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
            # check that forminfo is dictionary with sensible year ranges
            forminfo = variable['form']
            assert isinstance(forminfo, dict)
            yranges = sorted(forminfo.keys())
            num_yranges = len(yranges)
            prior_eyr = first_year - 1
            yrange_num = 0
            for yrange in yranges:
                yrange_num += 1
                yrlist = yrange.split('-')
                fyr = int(yrlist[0])
                if yrlist[1] == '20??':
                    indefinite_yrange = True
                    assert yrange_num == num_yranges
                else:
                    indefinite_yrange = False
                    eyr = int(yrlist[1])
                    if fyr != (prior_eyr + 1):
                        msg1 = '{} fyr {}'.format(vname, fyr)
                        msg2 = '!= prior_eyr_1 {}'.format(prior_eyr + 1)
                        assert msg1 == msg2
                    if eyr > last_form_year:
                        msg1 = '{} eyr {}'.format(vname, eyr)
                        msg2 = '> last_form_year {}'.format(last_form_year)
                        assert msg1 == msg2
                    prior_eyr = eyr
            if not indefinite_yrange and len(yranges) > 0:
                assert prior_eyr == last_form_year
