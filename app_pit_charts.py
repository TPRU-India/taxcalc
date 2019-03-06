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
import matplotlib.pyplot as plt

 
# Generate Charts
# first merge the files
START_YEAR = 2017
END_YEAR = 2023

year = START_YEAR
a={}
for year in range(START_YEAR, END_YEAR+1):
    filename1='dist-table-all-clp-avg-'+str(year)+'.txt'
    df1 = pd.read_fwf(filename1)       
    df1.drop('Unnamed: 0',axis=1,inplace=True)
    col_list =  df1.columns[1:] + '_avg_clp_' + str(year)
    col_list = col_list.insert(0, 'Income_Bracket')
    df1.columns = col_list
    filename2='dist-table-all-clp-total-'+str(year)+'.txt'
    df2 = pd.read_fwf(filename2)       
    df2.drop('Unnamed: 0',axis=1,inplace=True)
    col_list =  df2.columns[1:] + '_total_clp_' + str(year)
    col_list = col_list.insert(0, 'Income_Bracket')
    df2.columns = col_list
    a[year] = pd.merge(df1, df2, how="inner", on="Income_Bracket")
    filename3='dist-table-all-ref-avg-'+str(year)+'.txt'
    df3 = pd.read_fwf(filename3)       
    df3.drop('Unnamed: 0',axis=1,inplace=True)
    col_list =  df3.columns[1:] + '_avg_ref_' + str(year)
    col_list = col_list.insert(0, 'Income_Bracket')
    df3.columns = col_list
    a[year] = pd.merge(a[year], df3, how="inner", on="Income_Bracket")
    filename4='dist-table-all-ref-total-'+str(year)+'.txt'
    df4 = pd.read_fwf(filename4)       
    df4.drop('Unnamed: 0',axis=1,inplace=True)
    col_list =  df4.columns[1:] + '_total_ref_' + str(year)
    col_list = col_list.insert(0, 'Income_Bracket')
    df4.columns = col_list
    a[year] = pd.merge(a[year], df4, how="inner", on="Income_Bracket")

df=a[START_YEAR]
for year in range(START_YEAR+1, END_YEAR+1):
    df = pd.merge(df, a[year], how="inner", on="Income_Bracket")

df.set_index('Income_Bracket', inplace=True)

df.to_csv('dist-table-all-years.csv', index=True)

df = pd.read_csv('dist-table-all-years.csv')
df.set_index('Income_Bracket', inplace=True)
df_pit_totals_clp = df[df.columns[df.columns.str.startswith('pitax_total_clp')]]
df_pit_totals_ref = df[df.columns[df.columns.str.startswith('pitax_total_ref')]]
clp_pitax_list = df_pit_totals_clp.loc['ALL'].tolist()
clp_pitax_list = [float(i.replace(',','')) for i in clp_pitax_list]
clp_pitax_list = [round(elem, 0) for elem in clp_pitax_list ]
ref_pitax_list = df_pit_totals_ref.loc['ALL'].tolist()
ref_pitax_list = [float(i.replace(',','')) for i in ref_pitax_list]
ref_pitax_list = [round(elem, 0) for elem in ref_pitax_list ]
years = [x[-4:] for x in list(df_pit_totals_clp.columns)]

plt.style.use('seaborn-whitegrid')
fig = plt.figure()
"""
ax = plt.axes()
ax.plot(x, np.sin(x))
ax.set(xlim=(0, 10), ylim=(-2, 2),
       xlabel='x', ylabel='sin(x)',
       title='A Simple Plot')
"""
#plt.axis([2017, 2021, 150000, 400000])
plt.title("Estimated Tax Collection")
plt.xlabel("Year")
plt.ylabel("Tax Collection in lakh Cr.");
"""
print(year)
print(clp_pitax_list)
print(ref_pitax_list)
"""
plt.plot(years, clp_pitax_list, linestyle='-', marker='o', color='b', label='Current Law', linewidth=2.0)
plt.plot(years, ref_pitax_list, linestyle='--', marker='o', color='r', label='Reform', linewidth=2.0)
plt.legend(loc='best')
plt.savefig('Total_collection_PIT.png')
plt.show()
# plt.plot(years, clp_pitax_list, 'bo', years, ref_pitax_list, ':r', linewidth=2.0)
