import os
import numpy
import pandas
import pytest


# convert all numpy warnings into errors so they can be detected in tests
numpy.seterr(all='raise')


@pytest.fixture(scope='session')
def tests_path():
    return os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope='session')
def pit_path(tests_path):
    return os.path.join(tests_path, '..', 'pit.csv')


@pytest.fixture(scope='session')
def pit_fullsample(pit_path):
    return pandas.read_csv(pit_path)


@pytest.fixture(scope='session')
def pit_subsample(pit_fullsample):
    # TODO: when have larger pit_fullsample, draw fractional sample
    return pit_fullsample.sample(frac=1.00, random_state=123456789)
