Coding Style
============

This description of TPRU-India taxcalc coding style is written for a
person who wants to contribute changes to taxcalc source code.
It assumes that you have read the [USA Tax-Calculator Contributor
Guide](https://github.com/PSLmodels/Tax-Calculator/blob/master/docs/docs/contributing/contributor_guide.md),
have cloned the [central GitHub taxcalc
repository](https://github.com/TPRU-India/taxcalc)
to your GitHub account and to your local computer, and are familiar
with how to prepare a pull request for consideration by the core
development team.  This document describes the coding style you should
follow when preparing a pull request on your local computer.  By coding
style we mean primarily the vertical and horizontal spacing of the
code and the naming of new variables.

You main objective is to write Python code that is indistinguishable
in style from existing code in the repository.  In other words, after
your new code is merged with existing code it should be difficult for
somebody else to determine what you contributed.

In order to achieve this objective any new policy parameter names must
comply with the TPRU naming conventions.

In addition, any new or revised code must meet certain coding style
guidelines.

There are two recommended tools that can help you develop seamless and
correct code enhancements.

pycodestype (the program formerly known as pep8)
------------------------------------------------

One of these tools, `pycodestyle`, enforces coding styles that are required
of all Python code in the repository, and therefore, all pull requests
are tested using the `pycodestyle` tool.  Pull requests that fail these
tests need to be revised before they can be merged into the
repository.  The most efficient way to comply with this coding style
requirement is to process each file containing revisions through
`pycodestyle` on your local computer before submitting your pull request.

Make sure you have an up-to-date version of `pycodestyle` installed on your
computer by entering at the operating system command line:
```
pycodestyle --version
```
If you get a no-such-command error, install `pycodestyle` as follows:
```
conda install pycodestyle
```
If you do have `pycodestyle` installed, but the version is before 2.4.0,
then get a more recent version as follows:
```
conda update pycodestyle
```
Once you have a current version of `pycodestyle` installed on your computer,
use the `pycodestyle` tool as follows:
```
pycodestyle records.py
```
where in the above example you want to check the coding style of your
proposed revisions to the `records.py` file.

In addition, if you are proposing revisions to one of the files in the
taxcalc directory that has a `.json` extension, you should use the
`pycodestyle` tool as follows:
```
pycodestyle --ignore=E501,E121 current_law_policy.json
```
where in the above example you want to check the coding style of your
proposed revisions to the `current_law_policy.json` file.

Note that you can easily check **all** the Python files in the
directory tree beginning with the `taxcalc` directory as follows:
```
cd taxcalc
pycodestyle .
```
or
```
pycodestyle taxcalc
```
