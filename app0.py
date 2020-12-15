"""
**Basic app for PIT Microsimulation**
app0.py illustrates use of TPRU-India taxcalc release 2.0.0
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

# create GSTRecords object containing gst.csv and gst_weights.csv input data
grecs = GSTRecords()

assert isinstance(grecs, GSTRecords)
assert grecs.data_year == 2017
assert grecs.current_year == 2017

# create CorpRecords object containing cit.csv and cit_weights.csv input data
crecs = CorpRecords()

assert isinstance(crecs, CorpRecords)
assert crecs.data_year == 2017
assert crecs.current_year == 2017

# create Policy object containing current-law policy
pol = Policy()

assert isinstance(pol, Policy)
assert pol.current_year == 2017

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs, corprecords=crecs,
                   gstrecords=grecs, verbose=False)

# NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
#       so we can continue to use pol and recs in this script without any
#       concern about side effects from Calculator method calls on calc1.

assert isinstance(calc1, Calculator)
assert calc1.current_year == 2017

calc1.calc_all()

weighted_tax1 = calc1.weighted_total('pitax')
total_weights = calc1.total_weight()
print(f'Total PIT Liability for 2017 (in Cr.) {weighted_tax1 * 1e-7:,.2f}')

dump_vars = ['FILING_SEQ_NO', 'AGEGRP', 'SALARIES', 'INCOME_HP',
             'Income_BP', 'TOTAL_INCOME_OS', 'Aggregate_Income',
             'TI_special_rates', 'tax_TI_special_rates', 'GTI', 'TTI', 'pitax']
dumpdf = calc1.dataframe(dump_vars)
column_order = dumpdf.columns

assert len(dumpdf.index) == calc1.array_len

dumpdf.to_csv('app0-dump.csv', columns=column_order,
              index=False, float_format='%.0f')
