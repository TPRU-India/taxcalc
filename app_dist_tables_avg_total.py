"""
app_dist_Tables00.py illustrates use of pitaxcalc-demo release 2.0.0
(India version).
USAGE: python app_dist_Tables00.py
"""
import locale
import pandas as pd
from taxcalc import *
import numpy as np
from babel.numbers import format_currency

def remove_decimal(S):
    S = str(S)
    S = S[:-3]
    return S

def ind_currency(curr):
    curr_str = format_currency(curr, 'INR', locale='en_IN').replace(u'\xa0', u' ')
    return(remove_decimal(curr_str))

def convert_df(df, cols):
    # breakup the dataframe into cols and others
    df1 = df[cols].copy(deep=True)
    cols_other = df.columns.difference(cols)
    df2 = df[cols_other].copy(deep=True)
    # strip the first row and make it into a list
    for i in range(len(df)):
        #print('i '+ str(i))
        row = df1.loc[i].values.tolist()
        #print(row)
        # take the list and build a new list element by element
        row1=[]
        for j in range(len(row)):
            #row1.append(format_it(str(row[i])))
            #row1.append(format_it(row[i]))
            #value_str = format_currency(row[j], 'INR', locale='en_IN').replace(u'\xa0', u' ')
            value_str = ind_currency(row[j])
            row1.append(value_str)
        # replace the row with the changed list
        df1.loc[i] =  row1
        # reassemble the dataframe
    df = pd.concat([df2, df1], axis=1)     
    return(df)



# create Records object containing pit.csv and pit_weights.csv input data
recs = Records(data='pit.csv', weights='pit_weights.csv')
grecs = GSTRecords()
crecs = CorpRecords()

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs, gstrecords=grecs, corprecords=crecs, verbose=False)

# specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('Budget2019_reform.json', None)
#print(reform['policy'])
pol.implement_reform(reform['policy'])

calc2 = Calculator(policy=pol, records=recs, gstrecords=grecs, corprecords=crecs, verbose=False)
# loop through years 2017, 2018, 2019, and 2020 and print out pitax

START_YEAR = 2017
END_YEAR = 2023
BASE_YEAR = 2019
wtd_tax_clp={}
wtd_tax_ref={}
wtd_tot={}
for year in range(START_YEAR, END_YEAR+1):
    calc1.advance_to_year(year)
    calc2.advance_to_year(year)
    calc1.calc_all()
    calc2.calc_all()
    weighted_tax1 = calc1.weighted_total('pitax')
    weighted_tax2 = calc2.weighted_total('pitax')
    total_weights = calc1.total_weight()
    wtd_tax_clp[year] = weighted_tax1
    wtd_tax_ref[year] = weighted_tax2
    wtd_tot[year] = total_weights
    if (year>=BASE_YEAR):
        print(f'****************  Total Tax Collection for {year}', end=' ')
        print('****************')
        print('\n')
        print(f'Current Law: Tax Collection in Rs. Cr. for {year}:', end=' ')
        print(f'{weighted_tax1 * 1e-7:,.2f}')
        print(f'Reform     : Tax Collection in Rs. Cr. for {year}:', end=' ')
        print(f'{weighted_tax2 * 1e-7:,.2f}')
        print('               Difference in Tax Collection:', end=' ')
        print(f'{(weighted_tax2-weighted_tax1) * 1e-7:,.2f} Cr.')
        print('\n')
        print(f'Representing: {total_weights * 1e-5:,.2f} Lakh taxpayers')
        print('\n')
        for output_in_averages in [False, True]:
            output_categories = 'standard_income_bins'
            # pd.options.display.float_format = '{:,.3f}'.format
            # dt1, dt2 = calc1.distribution_tables(calc2, 'weighted_deciles')
            dt1, dt2 = calc1.distribution_tables(calc2, output_categories,
                                                 averages=output_in_averages,
                                                 scaling=True)
            dt2['pitax_diff'] = dt2['pitax'] - dt1['pitax']
            if (output_categories == 'standard_income_bins'):
                dt1.rename_axis('Income_Bracket', inplace=True)
                dt2.rename_axis('Income_Bracket', inplace=True)
            else:
                dt1.rename_axis('Decile', inplace=True)
                dt2.rename_axis('Decile', inplace=True)
            dt1 = dt1.reset_index().copy()
            dt2 = dt2.reset_index().copy()
            dt1 = dt1.fillna(0)
            dt2 = dt2.fillna(0)
            if output_in_averages:
                print('***************************  Average Tax Burden ', end=' ')
                print(f'(in Rs.) per Taxpayer for {year}  ***************************')
                pd.options.display.float_format = '{:,.0f}'.format
            else:
                print('*****************  Distribution Tables ', end=' ')
                print(f'for Total Tax Collection (in Rs. crores) for {year} *********')
                pd.options.display.float_format = '{:,.3f}'.format
            
            # list of columns for printing in rupees
            col_list1 = list(dt1.columns)
            col_list1.remove('Income_Bracket')
            col_list1.remove('weight')
            print('\n')
            print('  *** CURRENT-LAW DISTRIBUTION TABLE ***')
            #print('\n')
            print(convert_df(dt1, col_list1))
            print('\n')
            print('  *** POLICY-REFORM DISTRIBUTION TABLE ***')
            #print('\n')
            col_list2 = col_list1
            col_list2.append('pitax_diff')
            print(convert_df(dt2, col_list2))
            print('\n')
            # print text version of each complete distribution table to a file
            if output_in_averages:
                with open('dist-table-all-clp-avg-'+str(year)+'.txt', 'w') as dfile:
                    dt1.to_string(dfile)
                with open('dist-table-all-ref-avg-'+str(year)+'.txt', 'w') as dfile:
                    dt2.to_string(dfile)
                # print text version of each partial distribution table to a file
                to_include = ['weight', 'GTI', 'TTI', 'pitax']
                with open('dist-table-part-clp-avg-'+str(year)+'.txt', 'w') as dfile:
                    dt1.to_string(dfile, columns=to_include)
                with open('dist-table-part-ref-avg-'+str(year)+'.txt', 'w') as dfile:
                    dt2.to_string(dfile, columns=to_include)                
            else:
                with open('dist-table-all-clp-total-'+str(year)+'.txt', 'w') as dfile:
                    dt1.to_string(dfile)
                with open('dist-table-all-ref-total-'+str(year)+'.txt', 'w') as dfile:
                    dt2.to_string(dfile)
                # print text version of each partial distribution table to a file
                to_include = ['weight', 'GTI', 'TTI', 'pitax']
                with open('dist-table-part-clp-total-'+str(year)+'.txt', 'w') as dfile:
                    dt1.to_string(dfile, columns=to_include)
                with open('dist-table-part-ref-total-'+str(year)+'.txt', 'w') as dfile:
                    dt2.to_string(dfile, columns=to_include)

# Print the total taxes in the end

for year in range(BASE_YEAR, END_YEAR+1):
    wtd_tax_clp_rs = ind_currency(wtd_tax_clp[year] * 1e-7)
    wtd_tax_ref_rs = ind_currency(wtd_tax_ref[year] * 1e-7)
    wtd_tax_diff_rs = ind_currency((wtd_tax_ref[year]-wtd_tax_clp[year]) * 1e-7)
    print(f'****************  Total Tax Collection for {year}', end=' ')
    print('****************')
    #print('\n')
    print(f'Current Law: Tax Collection in Rs. Cr. for {year}:', end=' ')
    print(f'{ind_currency(wtd_tax_clp[year] * 1e-7)}')
    print(f'Reform     : Tax Collection in Rs. Cr. for {year}:', end=' ')
    print(f'{ind_currency(wtd_tax_ref[year] * 1e-7)}')
    print('                   Difference in Tax Collection:', end=' ')
    print(f'{ind_currency((wtd_tax_ref[year]-wtd_tax_clp[year]) * 1e-7)} Cr.')
    print(f'Representing: {wtd_tot[year] * 1e-5:,.2f} Lakh taxpayers')
    print('\n')

