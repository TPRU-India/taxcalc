"""
app1.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app2.py
"""
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

# create Records object containing pit.csv and pit_weights.csv input data
grecs = GSTRecords()

# create CorpRecords object containing cit.csv and cit_weights.csv input data
crecs = CorpRecords()

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs, gstrecords=grecs,
                   corprecords=crecs, verbose=False)

# specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('GST_reform.json', None)
pol.implement_reform(reform['policy'])
calc2 = Calculator(policy=pol, records=recs, gstrecords=grecs,
                   corprecords=crecs, verbose=False)

# loop through years 2017, 2018, and 2019 and print out pitax
for year in range(2017, 2020):
    print('\n')
    calc1.advance_to_year(year)
    calc2.advance_to_year(year)
    calc1.calc_all()
    id_gst1 = calc1.garray('ID_NO')
    gst_cereal1 = calc1.garray('gst_cereal')
    gst_other1 = calc1.garray('gst_other')
    gst_total1 = calc1.garray('gst')
    wgt_gst1 = calc1.garray('weight')
    total_gst1 = sum(gst_total1 * wgt_gst1) / 10**7
    print(f'Total GST collection - Current Law, {year}: {total_gst1:,.2f}')

    calc2.calc_all()
    id_gst2 = calc2.garray('ID_NO')
    gst_cereal2 = calc2.garray('gst_cereal')
    gst_other2 = calc2.garray('gst_other')
    gst_total2 = calc2.garray('gst')
    wgt_gst2 = calc2.garray('weight')
    total_gst2 = sum(gst_total2 * wgt_gst2) / 10**7
    print(f'Total GST collection - Reform, {year}     : {total_gst2:,.2f}')
