"""
app01.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app0.py > app0.res
CHECK: Use your favorite Windows diff utility to confirm that app0.res is
       the same as the app0.out file that is in the repository.
"""
import pandas as pd
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

grecs = GSTRecords()

# create CorpRecords object using cross-section data
crecs1 = CorpRecords(data='cit_cross.csv', weights='cit_cross_wgts.csv')

# create CorpRecords object using panel data
crecs2 = CorpRecords(data='cit_panel.csv', data_type='panel')

# create Policy object containing current-law polic
pol1 = Policy()
pol2 = Policy()
reform = Calculator.read_json_param_objects('app01_reform.json', None)
pol2.implement_reform(reform['policy'])

# specify Calculator objects for current-law policy
calc1c = Calculator(policy=pol1, records=recs, corprecords=crecs1,
                    gstrecords=grecs, verbose=False)
calc1p = Calculator(policy=pol1, records=recs, corprecords=crecs2,
                    gstrecords=grecs, verbose=False)
calc2c = Calculator(policy=pol2, records=recs, corprecords=crecs1,
                    gstrecords=grecs, verbose=False)
calc2p = Calculator(policy=pol2, records=recs, corprecords=crecs2,
                    gstrecords=grecs, verbose=False)

for year in range(2017, 2022):
    calc1c.advance_to_year(year)
    calc1p.advance_to_year(year)
    calc2c.advance_to_year(year)
    calc2p.advance_to_year(year)
    # Produce DataFrame of results using cross-section
    calc1c.calc_all()
    AggIncCB = calc1c.carray('GTI_Before_Loss')
    GTICB = calc1c.carray('GTI')
    TTICB = calc1c.carray('TTI')
    citaxCB = calc1c.carray('citax')
    wgtCB = calc1c.carray('weight')

    calc2c.calc_all()
    AggIncCR = calc2c.carray('GTI_Before_Loss')
    GTICR = calc2c.carray('GTI')
    TTICR = calc2c.carray('TTI')
    citaxCR = calc2c.carray('citax')
    wgtCR = calc2c.carray('weight')

    # Produce DataFrame of results using panel
    calc1p.calc_all()
    AggIncPB = calc1p.carray('GTI_Before_Loss')
    GTIPB = calc1p.carray('GTI')
    TTIPB = calc1p.carray('TTI')
    citaxPB = calc1p.carray('citax')
    wgtPB = calc1p.carray('weight')

    calc2p.calc_all()
    AggIncPR = calc2p.carray('GTI_Before_Loss')
    GTIPR = calc2p.carray('GTI')
    TTIPR = calc2p.carray('TTI')
    citaxPR = calc2p.carray('citax')
    wgtPR = calc2p.carray('weight')

    # print(f'Year  {year}: {weighted_tax1 * 1e-9:,.2f}')
    print(f'************* Year  {year}  *************')
    # print('*************Year  ' + str(year) + '   *************')
    print('GTI before loss, baseline, cross: ' +
          str(sum(AggIncCB * wgtCB) / 10**7))
    print('GTI, baseline, cross: ' + str(sum(GTICB * wgtCB) / 10**7))
    print('TTI, baseline, cross: ' + str(sum(TTICB * wgtCB) / 10**7))
    print('Tax, baseline, cross: ' + str(sum(citaxCB * wgtCB) / 10**7))
    print('\n')
    print('GTI before loss, reform, cross: ' +
          str(sum(AggIncCR * wgtCR) / 10**7))
    print('GTI, reform, cross: ' + str(sum(GTICR * wgtCR) / 10**7))
    print('TTI, reform, cross: ' + str(sum(TTICR * wgtCR) / 10**7))
    print('Tax, reform, cross: ' + str(sum(citaxCR * wgtCR) / 10**7))
    print('\n')
    print('Change in tax, cross: ' +
          str(sum((citaxCR - citaxCB) * wgtCB) / 10**7))
    print('\n')
    print('GTI before loss, baseline, panel: ' +
          str(sum(AggIncPB * wgtPB) / 10**7))
    print('GTI, baseline, panel: ' + str(sum(GTIPB * wgtPB) / 10**7))
    print('TTI, baseline, panel: ' + str(sum(TTIPB * wgtPB) / 10**7))
    print('Tax, baseline, panel: ' + str(sum(citaxPB * wgtPB) / 10**7))
    print('\n')
    print('GTI before loss, reform, panel: ' +
          str(sum(AggIncPR * wgtPR) / 10**7))
    print('GTI, reform, panel: ' + str(sum(GTIPR * wgtPR) / 10**7))
    print('TTI, reform, panel: ' + str(sum(TTIPR * wgtPR) / 10**7))
    print('Tax, reform, panel: ' + str(sum(citaxPR * wgtPR) / 10**7))
    print('\n')
    print('Change in tax, panel: ' +
          str(sum((citaxPR - citaxPB) * wgtPB) / 10**7))
    print('\n')
