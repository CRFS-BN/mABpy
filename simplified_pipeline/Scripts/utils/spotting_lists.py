"""
Functions for echo spotting lists

Author: Malwina Kotowicz
E-mail: malwina.kotowicz@dzne.de
"""

import pandas as pd

def get_tspotting_list(df_reference, cols, col_names, volume):
    
    """
    Creates pcr3 template spotting list. Gets exerpt of df_reference (specPCR list chunk) based on cols,
    renames cols to col_names, adds vol
    """
    
    tspotting = df_reference[cols] #get excerpt of specPCR list
    tspotting.loc[:, 'Volume'] = volume 
    for col_old, col_new in zip(cols,col_names):
        #rename each col to echo suitable
        tspotting = tspotting.rename(columns={col_old:col_new})
        
    return tspotting