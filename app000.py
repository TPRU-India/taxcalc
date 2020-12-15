"""
**Basic app for GST Microsimulation**
app000.py illustrates use of TPRU-India taxcalc release 2.0.0
USAGE: python app000.py > app000.res
CHECK: Use your favorite Windows diff utility to confirm that app000.res is
       the same as the app000.out file that is in the repository.
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

# Produce DataFrame of results using cross-section
calc1.calc_all()
id_gst = calc1.garray('ID_NO')
gst_cereal = calc1.garray('gst_cereal')
total_consumption = calc1.garray('total consumption')
gst_total = calc1.garray('gst')
wgt_gst = calc1.garray('weight')
weighted_gst_cereal = calc1.weighted_garray('gst_cereal')
weighted_gst = calc1.weighted_garray('gst')
weighted_consumption = calc1.weighted_garray('total consumption')
total_consumption_all = calc1.weighted_total_garray('total consumption')
total_consumption_all = total_consumption_all / 10**7
total_gst = calc1.weighted_total_garray('gst') / 10**7
total_weight = calc1.weighted_total_garray('weight') / 10**7
print(f'Total Consumption in Economy - 2017: {total_consumption_all:,.0f}')
print(f'Total GST Collection - 2017: {total_gst:,.0f}')
print(f'Total Weight - 2017: {total_weight:,.0f}')
results = pd.DataFrame({'GST_ID_NO': id_gst,
                        'Weight': wgt_gst,
                        'Weighted GST_Cereal': weighted_gst_cereal,
                        'Weighted Total Consumption': weighted_consumption,
                        'Weighted GST': weighted_gst})
results.to_csv('app000-dump-gst.csv', index=False,
               float_format='%.0f')
