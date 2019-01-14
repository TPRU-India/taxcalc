Testing Procedures
==================

This description of pitaxcalc-demo testing procedure is written for a
person who wants to contribute changes to pitaxcalc-demo source code.
It assumes that you have read the [USA Tax-Calculator Contributor
Guide](https://github.com/PSLmodels/Tax-Calculator/blob/master/CONTRIBUTING.md#tax-calculator-contributor-guide)
and have cloned the [central GitHub pitaxcalc-demo
repository](https://github.com/TPRU-demo/pitaxcalc-demo)
to your GitHub account and to your local computer, and are familiar
with how to prepare a pull request for consideration by the core
development team.  This document describes the testing procedure you
should follow on your local computer before submitting a development
branch as a pull request to the central pitaxcalc-demo repository at
GitHub.

Currently there are two phases of testing.

Testing with pycodetest (the program formerly known as pep8)
------------------------------------------------------------

The first phase of testing checks the formatting of the Python code
against the PEP8-like standard.  Assuming you are in the top-level
directory of the repository, do these tests either of these two ways:

```
cd taxcalc
pycodestyle .
```
or
```
pycodestyle taxcalc
```

No messages indicate the tests pass.  Fix any errors.  When you
pass all these PEP8-like tests, proceed to the second phase of testing.

Testing with pytest
--------------------

Run the second-phase of testing as follows at the command prompt in
the pitaxcalc-demo directory at the top of the repository directory
tree:

```
cd taxcalc
pytest -n4
```

This will start executing a pytest suite containing many tests.
Depending on your computer, the execution time for this suite of tests
is roughly one minute.  The `-n4` option calls for using as many as
four CPU cores for parallel execution of the tests.  If you want
sequential execution of the tests (which will take at least twice as
long to execute), simply omit the `-n4` option.

Interpreting the Test Results
-----------------------------

If you are adding an enhancement that expands the capabilities of
pitaxcalc-demo, then all the tests you can run should pass before you
submit a pull request containing the enhancement.  In addition, it
would be highly desirable to add a test to the pytest suite, which is
located in the ```taxcalc/tests``` directory, that somehow checks that
your enhancement is working as you expect it to work.

On the other hand, if you think you have found a bug in the
pitaxcalc-demo source code, the first thing to do is add a test to the
pytest suite that demonstrates how the source code produces an
incorrect result (that is, the test fails because the result is
incorrect).  Then change the source code to fix the bug and
demonstrate that the newly-added test, which used to fail, now passes.

Updating the Test Results
-------------------------

After an enhancement or bug fix, you may be convinced that the new and
different second-phase test results are, in fact, correct.  How do you
eliminate the test failures?  For all but a few tests, simply edit the
appropriate `taxcalc/tests/test_*.py` file so that the test passes
when you rerun `pytest`.
