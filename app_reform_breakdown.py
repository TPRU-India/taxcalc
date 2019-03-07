import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
import json
from taxcalc import *
from babel.numbers import format_currency
from collections import defaultdict

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

#reform = Calculator.read_json_param_objects('Budget2019_reform.json', None)

def run_calculator(reform, ref_num):
    # create Records object containing pit.csv and pit_weights.csv input data
    recs = Records(data='pit.csv', weights='pit_weights.csv')
    grecs = GSTRecords()
    crecs = CorpRecords()
    
    # create Policy object containing current-law policy
    pol = Policy()
    
    # specify Calculator object for current-law policy
    calc1 = Calculator(policy=pol, records=recs, gstrecords=grecs, corprecords=crecs, verbose=False)
    
    # specify Calculator object for reform in JSON file
    #print(reform['policy'])
    pol.implement_reform(reform['policy'])
    
    calc2 = Calculator(policy=pol, records=recs, gstrecords=grecs, corprecords=crecs, verbose=False)
    # loop through years 2017, 2018, 2019, and 2020 and print out pitax
    
    #START_YEAR = 2017
    #END_YEAR = 2023
    #BASE_YEAR = 2019
    reform_text = reform['policy']
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
            output_in_averages = False
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
               print('')
               #print('***************************  Average Tax Burden ', end=' ')
               #print(f'(in Rs.) per Taxpayer for {year}  ***************************')
               #print(f'For reform: {reform_text}')
               #pd.options.display.float_format = '{:,.0f}'.format
            else:
               print('')
               #print('*****************  Distribution Tables ', end=' ')
               #print(f'for Total Tax Collection (in Rs. crores) for {year} *********')
               #print(f'For reform: {reform_text}')
               #pd.options.display.float_format = '{:,.0f}'.format
                
            # list of columns for printing in rupees
            col_list1 = list(dt1.columns)
            col_list1.remove('Income_Bracket')
            col_list1.remove('weight')
            #print('\n')
            #print('  *** CURRENT-LAW DISTRIBUTION TABLE ***')
            #print('\n')
            #print(convert_df(dt1, col_list1))
            #print('\n')
            #print('  *** POLICY-REFORM DISTRIBUTION TABLE ***')
            #print('\n')
            col_list2 = col_list1
            col_list2.append('pitax_diff')
            #print(convert_df(dt2, col_list2))
            #print('\n')
            # print text version of each complete distribution table to a file
            if output_in_averages:
                with open('dist-table-all-clp-avg-'+str(year)+'.txt', 'w') as dfile:
                    dt1.to_string(dfile)
                with open('dist-table-all-ref-'+str(ref_num)+'-avg-'+str(year)+'.txt', 'w') as dfile:
                    dt2.to_string(dfile)
                # print text version of each partial distribution table to a file
                to_include = ['weight', 'GTI', 'TTI', 'pitax']
                with open('dist-table-part-clp-avg-'+str(year)+'.txt', 'w') as dfile:
                    dt1.to_string(dfile, columns=to_include)
                with open('dist-table-part-ref-'+str(ref_num)+'-avg-'+str(year)+'.txt', 'w') as dfile:
                    dt2.to_string(dfile, columns=to_include)                
            else:
                with open('dist-table-all-clp-total-'+str(year)+'.txt', 'w') as dfile:
                    dt1.to_string(dfile)
                with open('dist-table-all-ref-'+str(ref_num)+'-total-'+str(year)+'.txt', 'w') as dfile:
                    dt2.to_string(dfile)
                # print text version of each partial distribution table to a file
                to_include = ['weight', 'GTI', 'TTI', 'pitax']
                with open('dist-table-part-clp-total-'+str(year)+'.txt', 'w') as dfile:
                    dt1.to_string(dfile, columns=to_include)
                with open('dist-table-part-ref-'+str(ref_num)+'-total-'+str(year)+'.txt', 'w') as dfile:
                    dt2.to_string(dfile, columns=to_include)

def gen_reform(tdict):
    param_key_dict = dict(tdict)
    year_param = dict()
    for pkey, sdict in param_key_dict.items():
        #print(f'pkey: {pkey}')
        #print(f'sdict: {sdict}')
        rdict = dict()
        for skey, val in sdict.items():
            #print(f'skey: {skey}')
            #print(f'val: {val}')
            year = int(skey)
            rdict[year] = val
            #print(f'rdict: {rdict}')
        year_param[pkey] = rdict
        #print(f'year_param: {year_param}')
    year_key_dict = dict()
    years = set()
    for param, sdict in year_param.items():
        for year, val in sdict.items():
            if year not in years:
                years.add(year)
                year_key_dict[year] = dict()
                year_key_dict[year][param] = val
    
    rpol_dict = year_key_dict
    cons_dict = dict()
    behv_dict = dict()
    gdiff_base_dict = dict()
    gdiff_resp_dict = dict()
    growmodel_dict = dict()
    param_dict = dict()
    param_dict['policy'] = rpol_dict
    param_dict['consumption'] = cons_dict
    param_dict['behavior'] = behv_dict
    param_dict['growdiff_baseline'] = gdiff_base_dict
    param_dict['growdiff_response'] = gdiff_resp_dict
    param_dict['growmodel'] = growmodel_dict
    #print(param_dict)
    return param_dict

START_YEAR = 2017
END_YEAR = 2023
BASE_YEAR = 2019
        
txt = open('Budget2019_reform.json', 'r').read()
json_str = re.sub('//.*', ' ', txt)
raw_dict = json.loads(json_str)
tdict = Policy.translate_json_reform_suffixes(raw_dict['policy'])
#print(f'tdict: {tdict}')
list_tdict=list(tdict.items())
keys_tdict=list(tdict.keys())
ref_num = len(tdict)
for i in range(ref_num):
    #param_key_dict = tdict
    reform = gen_reform(list_tdict[i:i+1])
    run_calculator(reform, i)
    #print(f'reform: {ref}')


# Generate Charts
# first merge the files
year = BASE_YEAR

filename1='dist-table-all-clp-total-'+str(year)+'.txt'
df1 = pd.read_fwf(filename1)       
df1.drop('Unnamed: 0',axis=1,inplace=True)
df1 = df1[['Income_Bracket', 'pitax']]
col_list =  df1.columns[1:] + '_total_clp_' + str(year)
col_list = col_list.insert(0, 'Income_Bracket')
df1.columns = col_list
for year in range(BASE_YEAR+1, END_YEAR+1):
    filename2='dist-table-all-clp-total-'+str(year)+'.txt'
    df2 = pd.read_fwf(filename1)       
    df2.drop('Unnamed: 0',axis=1,inplace=True)
    df2 = df2[['Income_Bracket', 'pitax']]
    col_list =  df2.columns[1:] + '_total_clp_' + str(year)
    col_list = col_list.insert(0, 'Income_Bracket')
    df2.columns = col_list
    df1 = pd.merge(df1, df2, how="inner", on="Income_Bracket")    
            
for i in range(ref_num):
    for year in range(BASE_YEAR, END_YEAR+1):
        filename2='dist-table-all-ref-'+ str(i)+'-total-'+str(year)+'.txt'
        df2 = pd.read_fwf(filename2)       
        df2.drop('Unnamed: 0',axis=1,inplace=True)
        df2 = df2[['Income_Bracket', 'pitax_diff']]
        col_list =  df2.columns[1:] + '_total_ref_'+str(year)+'_'+ str(i)
        col_list = col_list.insert(0, 'Income_Bracket')
        df2.columns = col_list
        df1 = pd.merge(df1, df2, how="inner", on="Income_Bracket")

df1.set_index('Income_Bracket', inplace=True)

df1.to_csv('dist-table-all-years-all-ref.csv', index=True)

df = pd.read_csv('dist-table-all-years-all-ref.csv')
df.set_index('Income_Bracket', inplace=True)
a={}
for year in range(BASE_YEAR, END_YEAR+1):
     #print(year)
     df_pitax_diff_totals_ref = df[df.columns[df.columns.str.startswith('pitax_diff_total_ref_'+str(year))]]
     ref_pitax_diff_list = df_pitax_diff_totals_ref.loc['ALL'].tolist()
     #print(ref_pitax_diff_list)
     ref_pitax_diff_list = [round(elem) for elem in ref_pitax_diff_list]
     a[year] = ref_pitax_diff_list

years = list(range(BASE_YEAR,END_YEAR+1))
N = len(years)

year = BASE_YEAR  
ref=defaultdict(dict)
for j in range(ref_num):
    i=0
    for pkey, sdict in a.items():
        #print(f'pkey: {pkey}')
        #print(f'sdict: {sdict}')
        #print(sdict[j])
        ref[j][year+i] = sdict[j]
        i=i+1
reform={}
for i in range(ref_num):
    reform[i] = list(ref[i].values())

list_tdict[0][0][1:].upper()
list(list_tdict[0][1].keys())[0]
str(list(list_tdict[0][1].values())[0][0])
reform_desc=[]
for i in range(ref_num):
    part1 = list_tdict[i][0][1:].upper()
    part2 = list(list_tdict[i][1].keys())[0]
    part3 = str(list(list_tdict[i][1].values())[0][0])
    ref = (part1 + " in " + part2 +  "->" + part3)
    reform_desc.append(ref)

       
N = len(years)
width = 0.35 
fig, ax = plt.subplots(figsize=(9, 5))
p={}
bottom_num=np.zeros(N)
for i in range(ref_num):
    p[i] = plt.bar(years, reform[i], width, bottom=bottom_num, label="")
    bottom_num = np.array(bottom_num) + np.array(reform[i])

ax.invert_yaxis()   
ax.set_ylabel('Rupees in Crores.', fontweight="bold")
ax.set_xlabel('Year', fontweight="bold")
plt.legend(reform_desc, loc=2)
plt.suptitle('Composition of the Change to total tax collection', fontsize=16, fontweight="bold")
plt.savefig('Composition of Tax Changes due to Reforms.png') 
plt.show()
