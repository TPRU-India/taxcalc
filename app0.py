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

dump_vars = Records.USABLE_READ_VARS | Records.CALCULATED_VARS
dumpdf = calc1.dataframe(list(dump_vars))
column_order = sorted(dumpdf.columns)

assert len(dumpdf.index) == calc1.array_len

dumpdf.to_csv('app0-dump.res', columns=column_order,
              index=False, float_format='%.0f')

"""
iMac:pitaxcalc-demo mrh$ python app0.py
iMac:pitaxcalc-demo mrh$ awk -F, '{print $1,$5,$10}' app0-dump.res
AGEGRP TTI pitax
0 230000 0
0 281000 1550
0 301000 2550
0 329000 3950
0 373000 6150
0 450000 10000
0 492000 12100
0 654000 43300
1 682000 46400
2 2269000 480700
"""
