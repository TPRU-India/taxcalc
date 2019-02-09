"""
app1.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app1.py > app1.res
CHECK: Use your favorite Windows diff utility to confirm that app1.res is
       the same as the app1.out file that is in the repository.
"""
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

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

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs, gstrecords=grecs,
                   corprecords=crecs, verbose=False)
calc1.calc_all()

# specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('GST_reform.json', None)
pol.implement_reform(reform['policy'])
calc2 = Calculator(policy=pol, records=recs, gstrecords=grecs,
                   corprecords=crecs, verbose=False)
calc2.calc_all()


# dump out records
id_gst1 = calc1.garray('ID_NO')
gst_cereal1 = calc1.garray('gst_cereal')
gst_other1 = calc1.garray('gst_other')
gst_total1 = calc1.garray('gst')
wgt_gst1 = calc1.garray('weight')
total_gst1 = sum(gst_total1 * wgt_gst1) / 10**7
print(f'Total GST collection - Current Law, 2017: {total_gst1:,.2f}')

id_gst2 = calc2.garray('ID_NO')
gst_cereal2 = calc2.garray('gst_cereal')
gst_other2 = calc2.garray('gst_other')
gst_total2 = calc2.garray('gst')
wgt_gst2 = calc2.garray('weight')
total_gst2 = sum(gst_total2 * wgt_gst2) / 10**7
print(f'Total GST collection - Reform, 2017     : {total_gst2:,.2f}')


results = pd.DataFrame({'GST_ID_NO': id_gst2,
                        'Weight': wgt_gst2,
                        'GST_Cereal': gst_cereal2,
                        'GST_Cereal': gst_other2,
                        'GST_Total': gst_total2})
results.to_csv('app001-dump-gst.csv', index=False,
                     float_format='%.0f')
