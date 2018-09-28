"""
app345.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app345.py > app345.res

"""
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs)


# specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('app1_reform.json', None)
pol.implement_reform(reform['policy'])
calc2 = Calculator(policy=pol, records=recs)



# loop through years 2017, 2018 and 2019 and print out pitax
for year in range(2017, 2020):

	calc1.advance_to_year(year)
	calc2.advance_to_year(year)
	calc1.calc_all()
	calc2.calc_all()
	weighted_tax1 = calc1.weighted_total('pitax')
	weighted_tax2 = calc2.weighted_total('pitax')
	total_weights = calc1.total_weight()
	print(f'Tax 1 {weighted_tax1 * 1e-9:,.2f}')
	print(f'Tax 2 {weighted_tax2 * 1e-9:,.2f}')
	print(f'Total weight for {year}:{total_weights * 1e-6:,.2f}')

# dump out records for 2019
dump_vars = ['FILING_SEQ_NO', 'AGEGRP', 'SALARIES', 'INCOME_HP',
             'TOTAL_PROFTS_GAINS_BP', 'TOTAL_INCOME_OS', 'GTI', 'TTI']
dumpdf = calc1.dataframe(dump_vars)
dumpdf['pitax1'] = calc1.array('pitax')
dumpdf['pitax2'] = calc2.array('pitax')
dumpdf['pitax_diff'] = dumpdf['pitax2'] - dumpdf['pitax1']
column_order = dumpdf.columns

assert len(dumpdf.index) == calc1.array_len

dumpdf.to_csv('app1-dump.csv', columns=column_order,
              index=False, float_format='%.0f')
