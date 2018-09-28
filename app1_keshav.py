"""
app1_keshav.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app0.py > app0.res
CHECK: Use your favorite Windows diff utility to confirm that app0.res is
       the same as the app1_keshav.out file that is in the repository.
"""
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current law policy
calc1 = Calculator(policy=pol, records=recs)
calc1.calc_all()

#specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('app_usa_reform_keshav.json', None)
pol.implement_reform(reform['policy'])
calc2 = Calculator(policy=pol,records=recs)
calc2.calc_all()

# compare aggregate results from two calculators
weighted_tax1 = calc1.weighted_total('pitax')
weighted_tax2 = calc2.weighted_total('pitax')
total_weights = calc1.total_weight()
print('Tax1 in Rs. crore', weighted_tax1*1e-7)
print('Tax2 in Rs. crore', weighted_tax2*1e-7)
print('Total weight', total_weights)
