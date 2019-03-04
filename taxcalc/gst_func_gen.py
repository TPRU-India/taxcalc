"""
generator for gst functions.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import pandas as pd
import numpy as np


with open('taxcalc/gstrecords_variables.json') as vfile:
    vardict = json.load(vfile)

FIELD_VARS = list(k for k, v in vardict['read'].items()
                             if (v['type'] == 'int'
                                 or v['type'] == 'float'))

for v in FIELD_VARS:
    if (v.startswith('CONS_') and not(v.startswith('CONS_CEREAL'))
        and not (v.startswith('CONS_OTHER'))):
        str1 = v.replace('CONS', 'gst_rate').lower()
        
f = open("gst_func_generator.txt", "w")

@iterate_jit(nopython=True)
def gst_liability_other(gst_rate_other, CONS_OTHER, gst_other):
    """
    Calculates the gst paid on Other consumption
    """
    gst_other = gst_rate_other * CONS_OTHER
    return gst_other

#f.write('@iterate_jit(nopython=True)')
f.write('\n')
str1 ='def gst_liability_other(calc, '
str2 = v
str3 = ', gst_cereal):'
f.write(str1 + str2 + str3)
f.write('\n')
f.write('    """  ')
f.write('\n')
f.write('    Calculates the gst paid on Cereal consumption')
f.write('\n')
f.write('    """   ')
f.write('\n')
f.write('    gst_cereal = gst_rate_cereal * CONS_CEREAL')
f.write('\n')
f.write('    return gst_cereal')
f.write('\n')
f.write('\n')

f.close()
