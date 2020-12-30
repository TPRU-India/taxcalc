try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    longdesc = f.read()

version = '0.0.0'

config = {
    'description': 'Tax Microsimulation Model for India',
    'url': 'https://github.com/TPRU-India/taxcalc',
    'download_url': 'https://github.com/TPRU-India/taxcalc',
    'description': 'taxcalc',
    'long_description': longdesc,
    'version': version,
    'license': 'xxx',
    'packages': ['taxcalc'],
    'include_package_data': True,
    'name': 'taxcalc',
    'install_requires': ['numpy', 'pandas', 'numba'],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: xxx :: xxx',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    'tests_require': ['pytest']
}

setup(**config)
