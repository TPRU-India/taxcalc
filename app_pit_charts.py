"""
app_pit_charts.py illustrates use of TPRU-India taxcalc release 2.0.0
USAGE: python app_pit_charts.py
"""
import pandas as pd
from taxcalc import *
import numpy as np
from babel.numbers import format_currency
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

 
# Generate Charts
# first merge the files
START_YEAR = 2017
END_YEAR = 2023
BASE_YEAR = 2019
year = START_YEAR
a={}
for year in range(BASE_YEAR, END_YEAR+1):
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

df=a[BASE_YEAR]
for year in range(BASE_YEAR+1, END_YEAR+1):
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

# generating bar chart for difference in average tax burden due to reform 
# for 2020 - the first year of reform
year = 2020
df_pitax_diff = df['pitax_diff_avg_ref_'+str(year)]
df_pitax_diff = df_pitax_diff[:-1]
df_pitax_diff = df_pitax_diff[2:]
df_pitax_diff = df_pitax_diff.reset_index()
pitax_inc_brac_list = df_pitax_diff['Income_Bracket'].tolist()
pitax_diff_list = df_pitax_diff['pitax_diff_avg_ref_'+str(year)].tolist()

pitax_diff_list = [float(i.replace(',','')) for i in pitax_diff_list]

plt.rcdefaults()
#plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots(figsize=(8, 5))
# Example data
x_pos = np.arange(len(pitax_inc_brac_list))
ax.bar(x_pos, pitax_diff_list, 
        color='green')
ax.set_xticks(x_pos)
ax.set_xticklabels(pitax_inc_brac_list)
#ax.invert_yaxis()  # labels read top-to-bottom
ax.set_ylabel('Rupees')
ax.set_xlabel('Income Bracket')
ax.invert_yaxis()
ax.set_title('Change in Average Tax Burden Due to Reform in 2020')
plt.savefig('Average Tax Burden Change.png')
plt.show()

# generating pie chart for contribution of tax by different income groups 
# for 2020 - the first year of reform

year = 2020
df_pitax_tot_clp = df['pitax_total_clp_'+str(year)]
df_pitax_tot_clp = df_pitax_tot_clp[:-1]
df_pitax_tot_clp = df_pitax_tot_clp[2:]
df_pitax_tot_clp = df_pitax_tot_clp.reset_index()
pitax_inc_brac_list_clp = df_pitax_tot_clp['Income_Bracket'].tolist()
pitax_tot_list_clp = df_pitax_tot_clp['pitax_total_clp_'+str(year)].tolist()
pitax_tot_list_clp = [float(i.replace(',','')) for i in pitax_tot_list_clp]
pitax_tot_list_clp = [round(elem) for elem in pitax_tot_list_clp ]

fig, ax = plt.subplots(figsize=(10, 10))
# only "explode" the 5th slice (contributing to max revenue)
explode = (0, 0, 0, 0, 0.1, 0, 0, 0, 0)  

ax.pie(pitax_tot_list_clp, explode=explode, labels=pitax_inc_brac_list_clp, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.suptitle('Contribution by Income Bracket to total PIT in 2020', fontsize=16, fontweight="bold")
ax.set_title('Current Law', fontsize=16, fontweight="bold")
plt.savefig('Contribution to total PIT.png')
plt.show()

# generating pie chart for comparing contribution of tax by 
# different income groups for clp and reform for 2020 - the first year of reform



year = 2020
df_pitax_tot = df['pitax_total_ref_'+str(year)]
df_pitax_tot = df_pitax_tot[:-1]
df_pitax_tot = df_pitax_tot[2:]
df_pitax_tot = df_pitax_tot.reset_index()
pitax_inc_brac_list = df_pitax_tot['Income_Bracket'].tolist()
pitax_tot_list = df_pitax_tot['pitax_total_ref_'+str(year)].tolist()
pitax_tot_list = [float(i.replace(',','')) for i in pitax_tot_list]
pitax_tot_list = [round(elem) for elem in pitax_tot_list ]


fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10, 5))
#fig, ax = plt.subplots(figsize=(10, 5))
#the_grid = GridSpec(2, 2)

# only "explode" the 5th slice (contributing to max revenue)
explode = (0, 0, 0, 0, 0.1, 0, 0, 0, 0)  

#plt.subplot(the_grid[1, 0], aspect=1)
plt.suptitle('Contribution by Income Bracket to total PIT in 2020', fontsize=16, fontweight="bold")
ax1.pie(pitax_tot_list_clp, explode=explode, labels=pitax_inc_brac_list_clp, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

#plt.subplot(the_grid[0, 1], aspect=1)
ax2.pie(pitax_tot_list, explode=explode, labels=pitax_inc_brac_list, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('Current Law', fontweight="bold")
ax2.set_title('Reform', fontweight="bold")
plt.savefig('Contribution to total PIT - Before and After Reform.png')
plt.show()




