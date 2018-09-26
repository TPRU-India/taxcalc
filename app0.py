"""
app0.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app0.py > app0.res
CHECK: Use your favorite Windows diff utility to confirm that app0.res is
       the same as the app0.out file that is in the repository.
"""
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

assert isinstance(recs, Records)
assert recs.data_year == 2017
assert recs.current_year == 2017

# create Policy object containing current-law policy
pol = Policy()

assert isinstance(pol, Policy)
assert pol.current_year == 2017

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs)

# NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
#       so we can continue to use pol and recs in this script without any
#       concern about side effects from Calculator method calls on calc1.

assert isinstance(calc1, Calculator)
assert calc1.current_year == 2017

calc1.calc_all()

dump_vars = ['FILING_SEQ_NO', 'AGEGRP', 'SALARIES', 'INCOME_HP',
             'TOTAL_PROFTS_GAINS_BP', 'TOTAL_INCOME_OS', 'GTI', 'TTI', 'pitax']
dumpdf = calc1.dataframe(dump_vars)
column_order = dumpdf.columns

assert len(dumpdf.index) == calc1.array_len

dumpdf.to_csv('app0-dump.csv', columns=column_order,
              index=False, float_format='%.0f')
