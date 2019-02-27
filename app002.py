"""
app1.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app2.py
"""
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

# create Records object containing pit.csv and pit_weights.csv input data
grecs = GSTRecords(data = 'gst_updated.csv', weights = 'gst_weights.csv')

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
    CONS_CEREAL = calc1.garray('CONS_CEREAL')
    CONS_OTHER = calc1.garray('CONS_OTHER')    
    gst_cereal1 = calc1.garray('gst_cereal')
    gst_other1 = calc1.garray('gst_other')
    gst_total1 = calc1.garray('gst')
    #gst_total1[np.isnan(gst_total1)] = 0
    wgt_gst1 = calc1.garray('weight')
    print(f'ID_NO, {id_gst1}')
    print(f'CONS_CEREAL, {CONS_CEREAL}')
    print(f'gst_cereal, {gst_cereal1}')
    print(f'CONS_OTHER, {CONS_OTHER}')
    print(f'gst_other, {gst_other1}')
    total_gst1 = calc1.weighted_total_garray('gst') / 10**7
    print(f'Total GST collection - Current Law, {year}: {total_gst1:,.2f}')

    calc2.calc_all()
    id_gst2 = calc2.garray('ID_NO')
    gst_cereal2 = calc2.garray('gst_cereal')
    gst_other2 = calc2.garray('gst_other')
    gst_total2 = calc2.garray('gst')
    #gst_total2[np.isnan(gst_total2)] = 0
    wgt_gst2 = calc2.garray('weight')
    #total_gst2 = sum(gst_total2 * wgt_gst2) / 10**7
    total_gst2 = calc2.weighted_total_garray('gst') / 10**7   
    print(f'Total GST collection - Reform, {year}     : {total_gst2:,.2f}')
