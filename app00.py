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

# create CorpRecords object using cross-section data
crecs1 = CorpRecords(data='cit_cross.csv', weights='cit_cross_wgts.csv')
assert isinstance(crecs1, CorpRecords)
assert crecs1.current_year == 2017

# create CorpRecords object using panel data
crecs2 = CorpRecords(data='cit_panel.csv', data_type='panel')
assert isinstance(crecs2, CorpRecords)
assert crecs2.current_year == 2017

# create Policy object containing current-law policy
pol = Policy()

assert isinstance(pol, Policy)
assert pol.current_year == 2017

# specify Calculator objects for current-law policy
calc1 = Calculator(policy=pol, records=recs, corprecords=crecs1)
calc2 = Calculator(policy=pol, records=recs, corprecords=crecs2)

# NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
#       so we can continue to use pol and recs in this script without any
#       concern about side effects from Calculator method calls on calc1.

assert isinstance(calc1, Calculator)
assert calc1.current_year == 2017
assert isinstance(calc2, Calculator)
assert calc2.current_year == 2017

calc1.calc_all()
calc1.increment_year()
calc1.calc_all()

calc2.calc_all()
calc2.increment_year()
calc2.calc_all()



