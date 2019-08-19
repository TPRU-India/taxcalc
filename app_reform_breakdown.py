import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
import json
from taxcalc import *
from babel.numbers import format_currency
from collections import defaultdict
import copy

def remove_decimal(S):
    S = str(S)
    S = S[:-3]
    return S

def ind_currency(curr):
    curr_str = format_currency(curr, 'INR', locale='en_IN').replace(u'\xa0', u' ')
    return(remove_decimal(curr_str))

def run_calculator(reform):
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

    wtd_tax_clp={}
    wtd_tax_ref={}
    wtd_tax_diff={}

    for year in range(START_YEAR, END_YEAR+1):
        calc1.advance_to_year(year)
        calc2.advance_to_year(year)
        calc1.calc_all()
        calc2.calc_all()
        wtd_tax_clp[year] = calc1.weighted_total('pitax')
        wtd_tax_ref[year] = calc2.weighted_total('pitax')
        wtd_tax_diff[year] = wtd_tax_ref[year] - wtd_tax_clp[year]
        
    return(wtd_tax_clp, wtd_tax_ref, wtd_tax_diff)    
    
def gen_reform(list_tdict):
    param_key_dict = dict(list_tdict)
    year_param = dict()
    for pkey, sdict in param_key_dict.items():
        #print(f'pkey: {pkey}')
        #print(f'sdict: {sdict}')
        rdict = dict()
        for skey, val in sdict.items():
            year = int(skey)
            rdict[year] = val
        year_param[pkey] = rdict
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
    #print(f'param_dict: {param_dict}')
    return param_dict

def get_reform_desc(list_tdict):
    ref_num = len(list_tdict)
    reform_desc = ""
    for i in range(ref_num):
        part1 = list_tdict[i][0][1:].upper()
        part2 = list(list_tdict[i][1].keys())[0]
        part3 = str(list(list_tdict[i][1].values())[0][0])
        ref = (part1 + " in " + part2 +  "->" + part3)
        reform_desc = reform_desc + ref + '\n'
    return(reform_desc)
    
    
START_YEAR = 2017
END_YEAR = 2023
BASE_YEAR = 2019

# check if Calculator object for reform in JSON file is valid
# using all the checks in the Calculator object
reform_file = 'Budget2019_reform.json'
  
txt = open(reform_file, 'r').read()
json_str = re.sub('//.*', ' ', txt)
raw_dict = json.loads(json_str)
tdict = Policy.translate_json_reform_suffixes(raw_dict['policy'])
list_tdict=list(tdict.items())
keys_tdict=list(tdict.keys())
ref_num = len(tdict)

reform_desc=[]
for i in range(ref_num):
    part1 = list_tdict[i][0][1:].upper()
    part2 = list(list_tdict[i][1].keys())[0]
    part3 = str(list(list_tdict[i][1].values())[0][0])
    ref = (part1 + " in " + part2 +  "->" + part3)
    reform_desc.append(ref)

wtd_tax_clp={}
wtd_tax_ref={}
wtd_tax_diff={}
wtd_tot={} 
reform={}
#reform_diff={}

# Calculating impact for full reform
"""
reform_overall = gen_reform(list_tdict)
run_calculator(reform_overall, ref_num=99, reform_desc=reform_desc_combined)
wtd_tax_clp['ref_99'], wtd_tax_ref['ref_99'], wtd_tax_diff['ref_99'], wtd_tot['ref_99'] = run_calculator(reform_overall, ref_num=99, reform_desc=reform_desc_combined)
d = dict((k, v) for k, v in wtd_tax_diff['ref_99'].items() if k >= BASE_YEAR)
reform_base = list(d.values())
reform_base = np.array(list(d.values()))
reform_base = np.round(reform_base/10**7)
reform_base = reform_base.astype(int)
"""
# Using stacking process, we first use one reform and then add subsequent reforms
#print('**********************************************')
   
list_tdict_orig = list_tdict[:]
for i in range(ref_num):
    list_tdict = list_tdict_orig[0:i+1]
    reform_dict = gen_reform(list_tdict)
    reform_desc_ref = get_reform_desc(list_tdict)
    ref='ref_'+str(i)
    wtd_tax_clp[ref], wtd_tax_ref[ref], wtd_tax_diff[ref] = run_calculator(reform_dict)
    for year in range(START_YEAR, END_YEAR+1):
        if (year>=BASE_YEAR):
            print('******')
            print(f'Current Law: Tax Collection in Rs. Cr. for {year}:', end=' ')
            print(f'{ind_currency(wtd_tax_clp[ref][year] * 1e-7)}')
            print(f'   Reform-> \n{reform_desc_ref}Reform: Tax Collection in Rs. Cr. for {year}:', end=' ')
            print(f'{ind_currency(wtd_tax_ref[ref][year] * 1e-7)}')        
            print('              Difference in Tax Collection:', end=' ')
            print(f'{ind_currency(wtd_tax_diff[ref][year] * 1e-7)} Cr.')

for i in range(ref_num):
    ref_tag='ref_'+str(i) 
    d = dict((k, v) for k, v in wtd_tax_diff[ref_tag].items() if k >= BASE_YEAR)
    reform[i] = np.array(list(d.values()))
    reform[i] = np.round(reform[i]/10**7)
    reform[i] = reform[i].astype(int)


for i in range(ref_num-1):
    reform[i+1] = reform[i+1] - reform[i]
    
years = list(range(BASE_YEAR,END_YEAR+1))
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
plt.suptitle('Composition of the Changes to Total Tax Collection', fontsize=16, fontweight="bold")
plt.savefig('Composition of Tax Changes due to Reforms.png') 
plt.show()