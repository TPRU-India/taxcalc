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
def gst_path(tests_path):
    return os.path.join(tests_path, '..', 'gst.csv')


@pytest.fixture(scope='session')
def cit_crosspath(tests_path):
    return os.path.join(tests_path, '..', 'cit_cross.csv')


@pytest.fixture(scope='session')
def cit_panelpath(tests_path):
    return os.path.join(tests_path, '..', 'cit_panel.csv')


@pytest.fixture(scope='session')
def pit_fullsample(pit_path):
    return pandas.read_csv(pit_path)


@pytest.fixture(scope='session')
def pit_subsample(pit_fullsample):
    # TODO: when have larger pit_fullsample, reduce value of frac
    return pit_fullsample.sample(frac=0.10, random_state=123456789)


@pytest.fixture(scope='session')
def gst_sample(gst_path):
    # TODO: when have larger pit_fullsample, reduce value of frac
    return pandas.read_csv(gst_path)


@pytest.fixture(scope='session')
def cit_crosssample(cit_crosspath):
    return pandas.read_csv(cit_crosspath)


@pytest.fixture(scope='session')
def cit_panelsample(cit_panelpath):
    return pandas.read_csv(cit_panelpath)
