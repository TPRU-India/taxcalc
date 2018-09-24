"""
Tests of Tax-Calculator GrowFactors class.
"""
# CODING-STYLE CHECKS:
# pycodestyle test_growfactors.py
# pylint --disable=locally-disabled test_growfactors.py

import os
import tempfile
import pytest
# pylint: disable=import-error
from taxcalc import GrowFactors, Records, Policy


@pytest.fixture(scope='module', name='bad_gf_file')
def fixture_bad_gf_file():
    """
    Fixture for invalid growfactors file.
    """
    txt = (u'YEAR,CPI,SALARY,RENT,BADNAME,DEDUCTION\n'
           u'2017,1.000,1.000,1.000,1.000,1.000\n')
    tfile = tempfile.NamedTemporaryFile(mode='a', delete=False)
    tfile.write(txt)
    tfile.close()
    # Must close and then yield for Windows platform
    yield tfile
    os.remove(tfile.name)


def test_improper_usage(bad_gf_file):
    """
    Tests of improper usage of GrowFactors object.
    """
    with pytest.raises(ValueError):
        gfo = GrowFactors(dict())
    with pytest.raises(ValueError):
        gfo = GrowFactors(bad_gf_file.name)
    gfo = GrowFactors()
    fyr = gfo.first_year
    lyr = gfo.last_year
    with pytest.raises(ValueError):
        gfo.price_inflation_rates(fyr - 1, lyr)
    with pytest.raises(ValueError):
        gfo.price_inflation_rates(fyr, lyr + 1)
    # with pytest.raises(ValueError):
    #     gfo.price_inflation_rates(lyr, fyr)
    with pytest.raises(ValueError):
        gfo.wage_growth_rates(fyr - 1, lyr)
    with pytest.raises(ValueError):
        gfo.wage_growth_rates(fyr, lyr + 1)
    # with pytest.raises(ValueError):
    #     gfo.wage_growth_rates(lyr, fyr)
    with pytest.raises(ValueError):
        gfo.factor_value('BADNAME', fyr)
    with pytest.raises(ValueError):
        gfo.factor_value('CPI', fyr - 1)
    with pytest.raises(ValueError):
        gfo.factor_value('SALARY', lyr + 1)


def test_proper_usage():
    """
    Test proper usage of GrowFactors object.
    """
    gfo = GrowFactors()
    pir = gfo.price_inflation_rates(2017, 2017)
    assert len(pir) == 1
    wgr = gfo.wage_growth_rates(2017, 2017)
    assert len(wgr) == 1


def test_growfactors_csv_values():
    """
    Test numerical contents of growfactors.csv file.
    """
    gfo = GrowFactors()
    min_data_year = min(2017, Records.PITCSV_YEAR)
    if min_data_year < Policy.JSON_START_YEAR:
        for gfname in GrowFactors.VALID_NAMES:
            val = gfo.factor_value(gfname, min_data_year)
            assert val == 1
