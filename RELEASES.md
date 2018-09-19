pitaxcalc-demo RELEASE HISTORY
==============================
Go [here](https://github.com/TPRU-demo/pitaxcalc-demo/pulls?q=is%3Apr+is%3Aclosed) for a complete commit history.

Release numbering attempts to comply with [semantic
versioning](https://semver.org/).


2018-09-19 Release 1.0.0
------------------------
(last merged pull request is
[#14](https://github.com/TPRU-demo/pitaxcalc-demo/pull/14))

**Initial version with data and tax logic for USA**

See
[app_usa.py](https://github.com/TPRU-demo/pitaxcalc-demo/blob/master/app_usa.py)
for an example of how to use release 1.0.0 to analyze the effects of a
tax reform.

Note that you can always open a branch on you local computer that contains
release 1.0.0 by executing this command:
```
git checkout -b b100 1.0.0
```
That command will leave you on the b100 branch.  When you're finished
using 1.0.0, be sure to checkout the master branch and then delete the
b100 branch:
```
git checkout master
git branch -d b100
```
