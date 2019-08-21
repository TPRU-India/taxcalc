import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

def run_calculator(year, data_file, weights_file):
    # create Records object containing pit.csv and pit_weights.csv input data
    recs = Records(data=data_file, weights=weights_file)
    grecs = GSTRecords()
    crecs = CorpRecords()
    
    # create Policy object containing current-law policy
    pol = Policy()
    
    # specify Calculator object for current-law policy
    calc1 = Calculator(policy=pol, records=recs, gstrecords=grecs, corprecords=crecs, verbose=False)
    
    calc1.advance_to_year(year)
    calc1.calc_all()
    pit_df=calc1.dataframe(['FILING_SEQ_NO', 'AGE', 'weight', 'GTI', 'pitax'])
       
    return(pit_df)    
    
    
START_YEAR = 2017
END_YEAR = 2023
BASE_YEAR = 2019

year=2017

data_file ='taxcalc/pitSmallData.csv'
data_file_1 ='taxcalc/pitSmallData_1.csv'
#data_file ='taxcalc/pit.csv'
#data_file_1 ='taxcalc/pit_1.csv'
weights_file ='pit_weightsSD.csv'
#weights_file ='pit_weights.csv'
delta = 1
pit_orig_df = pd.read_csv(data_file)
pit_orig_1_df=pit_orig_df.copy()
pit_orig_1_df['SALARIES'] = pit_orig_1_df['SALARIES']+ delta
pit_orig_1_df.to_csv(data_file_1)
data_file ='pitSmallData.csv'
data_file_1 ='pitSmallData_1.csv'
#data_file ='pit.csv'
#data_file_1 ='pit_1.csv'

pit_df = run_calculator(year, data_file, weights_file)
pit_1_df = run_calculator(year, data_file_1, weights_file)
pit_1_df = pit_1_df.rename(columns={'weight':'weight_1', 'GTI':'GTI_1', 'pitax':'pitax_1'})
pit_1_df.drop('AGE', axis=1, inplace=True)

pit_df = pd.merge(pit_df, pit_1_df, how="inner", on='FILING_SEQ_NO')
pit_df['MTR_Labor'] = (pit_df['pitax_1'] - pit_df['pitax'])/delta

pit_df['ETR'] = pit_df['pitax']/pit_df['GTI']

pit_1_df = pit_df.copy()

sns.distplot(tuple(pit_df['MTR_Labor']), hist = False, kde = True, 
             kde_kws = {'linewidth': 3}, label = "MTR")

pit_df['ETR'] = pit_df['pitax']/pit_df['GTI']

pit_clean_df = pit_df.copy()
pit_df = pit_df[pit_df["MTR_Labor"]>-10]
pit_df = pit_df[pit_df["MTR_Labor"]<50]
pit_df = pit_df[pit_df["GTI"]<10000000]
pit_df = pit_df[pit_df["ETR"]<1]

pit_df.plot.scatter(x="GTI", y="MTR_Labor")
pit_df.plot.scatter(x="GTI", y="ETR")



