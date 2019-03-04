"""
app1.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app2.py
"""
from babel.numbers import format_currency
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

# create Records object containing pit.csv and pit_weights.csv input data
grecs = GSTRecords(data='gst.csv', weights='gst_weights.csv')

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
    total_consumption1 = calc1.garray('total consumption')
    gst_total1 = calc1.garray('gst')
    wgt_gst1 = calc1.garray('weight')
    weighted_gst_cereal1 = calc1.weighted_garray('gst_cereal')
    weighted_gst1 = calc1.weighted_garray('gst')
    weighted_consumption = calc1.weighted_garray('total consumption')
    total_consumption_all1 = calc1.weighted_total_garray('total consumption')
    total_consumption_all1 = total_consumption_all1 / 10**7
    total_gst1 = calc1.weighted_total_garray('gst') / 10**7
    total_weight1 = calc1.weighted_total_garray('weight') / 10**7
    total_consumption_all1_inr = format_currency(total_consumption_all1, 'INR', locale='en_IN').replace(u'\xa0', u' ')
    total_consumption_all1_inr_rs = total_consumption_all1_inr[:-3]
    total_gst1_inr = format_currency(total_gst1, 'INR', locale='en_IN').replace(u'\xa0', u' ')
    total_gst1_inr_rs = total_gst1_inr[:-3]
    print(f'*****  Due to Current Law in {year} *****')
    print(f'Total Consumption in - {year}: {total_consumption_all1_inr_rs} Cr.')
    print(f'Total GST Potential in - {year}: {total_gst1_inr_rs} Cr.')
    print(f'Total Number of Households in - {year}: {total_weight1:,.0f}')

    calc2.calc_all()
    id_gst2 = calc2.garray('ID_NO')
    gst_cereal2 = calc2.garray('gst_cereal')
    total_consumption2 = calc2.garray('total consumption')
    gst_total2 = calc2.garray('gst')
    wgt_gst2 = calc2.garray('weight')
    weighted_gst_cereal2 = calc2.weighted_garray('gst_cereal')
    weighted_gst2 = calc2.weighted_garray('gst')
    weighted_consumption = calc2.weighted_garray('total consumption')
    total_consumption_all2 = calc2.weighted_total_garray('total consumption')
    total_consumption_all2 = total_consumption_all2 / 10**7
    total_gst2 = calc2.weighted_total_garray('gst') / 10**7
    total_weight2 = calc2.weighted_total_garray('weight') / 10**7
    total_consumption_all2_inr = format_currency(total_consumption_all2, 'INR', locale='en_IN').replace(u'\xa0', u' ')
    total_consumption_all2_inr_rs = total_consumption_all2_inr[:-3]
    total_gst2_inr = format_currency(total_gst2, 'INR', locale='en_IN').replace(u'\xa0', u' ')
    total_gst2_inr_rs = total_gst2_inr[:-3]
    print(f'*****  Due to Reform in {year} *****')
    print(f'Total Consumption in - {year}: {total_consumption_all2_inr_rs} Cr.')
    print(f'Total GST Potential in - {year}: {total_gst2_inr_rs} Cr.')
    print(f'Total Number of Households in - {year}: {total_weight2:,.0f}')
