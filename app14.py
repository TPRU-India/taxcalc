"""
app14.py illustrates use of TPRU-India taxcalc release 2.0.0
USAGE: python app14.py
"""
import locale
from taxcalc import *


def gti_format(gti):
    str_gti = str(gti)
    str_gti = str_gti.replace('(', '')
    str_gti = str_gti.replace(']', '')
    split_gti = str_gti.split(', ')
    float1 = int(float(split_gti[0]))
    float2 = int(float(split_gti[1]))
    lc1 = locale.currency(float1, grouping=True)
    lc1 = lc1.replace('? ', '')
    lc2 = locale.currency(float2, grouping=True)
    lc2 = lc2.replace('? ', '')
    pt1 = f'{lc1}'
    pt2 = f'{lc2}'
    final_str = f'Rs. {pt1:16} - {pt2:15}'
    return final_str


locale.setlocale(locale.LC_ALL, '')

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records(data='pitBigData.csv', weights='pit_weightsBD.csv')

# create CorpRecords object containing cit.csv and cit_weights.csv input data
crecs = CorpRecords()

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs, corprecords=crecs, verbose=False)

# specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('app14_reform.json', None)
pol.implement_reform(reform['policy'])
calc2 = Calculator(policy=pol, records=recs, corprecords=crecs, verbose=False)
# loop through years 2017, 2018, and 2019 and print out pitax
for year in range(2017, 2020):
    calc1.advance_to_year(year)
    calc2.advance_to_year(year)
    calc1.calc_all()
    calc2.calc_all()
    weighted_tax1 = calc1.weighted_total('pitax')
    weighted_tax2 = calc2.weighted_total('pitax')
    total_weights = calc1.total_weight()
    print(f'Tax 1 for {year}: {weighted_tax1 * 1e-9:,.2f}')
    print(f'Tax 2 for {year}: {weighted_tax2 * 1e-9:,.2f}')
    print(f'Total weight for {year}: {total_weights * 1e-6:,.2f}')

# dump out records for 2019
dump_vars = ['FILING_SEQ_NO', 'AGEGRP', 'SALARIES', 'INCOME_HP',
             'TOTAL_PROFTS_GAINS_BP', 'TOTAL_INCOME_OS', 'GTI', 'TTI']
dumpdf = calc1.dataframe(dump_vars)
dumpdf['pitax1'] = calc1.array('pitax')
dumpdf['pitax2'] = calc2.array('pitax')
dumpdf['pitax_diff'] = dumpdf['pitax2'] - dumpdf['pitax1']
dumpdf['percent change in tax'] = np.where(dumpdf['pitax_diff'] == 0.0,
                                           0.0, (dumpdf['pitax_diff'] /
                                                 dumpdf['pitax1'] * 100))
dumpdf['Zero change'] = np.where(dumpdf['percent change in tax'] == 0.0, 1, 0)
column_order = dumpdf.columns

assert len(dumpdf.index) == calc1.array_len

dumpdf.to_csv('app14-dump.csv', columns=column_order,
              index=False, float_format='%.0f')
pd.options.display.float_format = 'Rs.{:,.0f}'.format
# converting the result into deciles and getting mean of 3 variables each yr
df1 = dumpdf.groupby(pd.qcut(dumpdf.GTI, 10))['pitax1', 'pitax2',
                                              'pitax_diff'].mean()
# making it more beautiful
renames = {'pitax1': 'Base', 'pitax2': 'Reform', 'pitax_diff': 'Difference'}
df1 = df1.reset_index()
df1['GTI'] = df1['GTI'].apply(gti_format)
df1.rename(renames, axis=1, inplace=True)
df1.index = [i for i in range(1, 11)]
print('\nIndividual Level - Average by Decile 2019')
print(df1)
df1.to_csv('Decilemeans.csv')  # conversion to csv files

df2 = dumpdf.groupby(pd.qcut(dumpdf.GTI, 10))['pitax1', 'pitax2',
                                              'pitax_diff'].sum()
df2 = df2.reset_index()
df2['GTI'] = df2['GTI'].apply(gti_format)
df2.rename(renames, axis=1, inplace=True)
df2.index = [i for i in range(1, 11)]
print('\nAggregate Tax Liability by Decile 2019')
print(df2)
df2.to_csv('Decilesum.csv')
