# CODING-STYLE CHECKS:
# pycodestyle test_policy.py

import os
import sys
import json
import tempfile
import numpy as np
import pytest
from taxcalc import Policy, Calculator


def test_incorrect_Policy_instantiation():
    with pytest.raises(ValueError):
        Policy(gfactors=list())
    with pytest.raises(ValueError):
        Policy(start_year=2000)
    with pytest.raises(ValueError):
        Policy(num_years=0)


def test_correct_Policy_instantiation():
    pol = Policy()
    assert pol
    pol.implement_reform({})
    with pytest.raises(ValueError):
        pol.implement_reform(list())
    with pytest.raises(ValueError):
        pol.implement_reform({2099: {'_rate2': [0.07]}})
    pol.set_year(2018)
    with pytest.raises(ValueError):
        pol.implement_reform({2017: {'_rate2': [0.07]}})
    with pytest.raises(ValueError):
        pol.implement_reform({2019: {'_rate2': [-0.10]}})


def test_inflation_rates():
    pol = Policy()  # automatically includes embedded GrowFactors object
    syr = pol.current_year
    assert syr == 2017
    # extract price inflation rates as specified in growfactors.csv file
    irates = pol.inflation_rates()
    assert irates[2017 - syr] == 0.045
    assert irates[2018 - syr] == 0.045
    assert irates[2019 - syr] == 0.045


REFORM0_CONTENTS = """
// Example of reform file suitable for Calculator read_json_param_objects().
// This JSON file can contain any number of trailing //-style comments, which
// will be removed before the contents are converted from JSON to a dictionary.
// The primary keys are policy parameters and secondary keys are years.
// Both the primary and secondary key values must be enclosed in quotes (").
// Boolean variables are specified as true or false (no quotes; all lowercase).
//
// Reform below increases the rebate ceiling from 5000 to 6000 in 2017 and
// then CPI-indexes the 6000 ceiling amount in subsequent years (i.e., 2018+).
//
{
    "policy": {
        "_rebate_ceiling": {
            "2017": [6000]  // increase current-law 2017 value
        },
        "_rebate_ceiling_cpi": {  // rebate_ceiling indexing status
            "2017": true  // values in future years indexed to CPI inflation
        }
    }
}
"""


@pytest.fixture(scope='module', name='reform0_file')
def fixture_reform0_file():
    """
    Temporary reform file for Calculator read_json_param_objects() function.
    """
    with tempfile.NamedTemporaryFile(mode='a', delete=False) as rfile:
        rfile.write(REFORM0_CONTENTS)
    # must close and then yield for Windows platform
    yield rfile
    if os.path.isfile(rfile.name):
        try:
            os.remove(rfile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


def test_read_json_param_and_implement_reform(reform0_file):
    """
    Test reading and translation of reform file into a reform dictionary
    that is then used to call implement_reform method.
    """
    policy = Policy()
    param_dict = Calculator.read_json_param_objects(reform0_file.name, None)
    policy.implement_reform(param_dict['policy'])
    syr = policy.start_year
    assert syr == 2017
    rebate_ceiling = policy._rebate_ceiling
    # assert rebate_ceiling[2017 - syr] == 6000
    # assert rebate_ceiling[2018 - syr] > 6000  # because value is CPI indexed
    # assert rebate_ceiling[2019 - syr] > rebate_ceiling[2018 - syr]
