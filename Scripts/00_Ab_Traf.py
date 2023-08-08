'''
WF parts: Antibody, transfection

Author: Malwina Kotowicz
E-mail: malwina.kotowicz@dzne.de
'''

import pandas as pd
import numpy as np
import os
from config import (dir_plasmid_id, dir_sorter, dir_ab1_output, WS_col_sort, dir_ass_imports,
                    WS_to_drop, WS_reshaped)
from utils.sorters import sort_categorically
from datetime import datetime
import argparse
import warnings

def transpose_WS(df,cols_to_drop,cols_reshaped):
    """Drops cols not needed after transposition (cols_to_drop), rehapes df using cols_reshaped col names"""
    df = df.drop(columns=cols_to_drop)
    df = pd.DataFrame(np.reshape(df.values,(-1,len(df.columns)*2)), columns=cols_reshaped)
    return df

def add_date_barcode(df,date_col,date_val,barcode_col, barcode_val):
    """Adds transfection date  & barcode to specified cols"""
    df[date_col] = date_val
    df[barcode_col] = barcode_val
    return df

if __name__ == '__main__':

    #silence future warning 
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-d','--trans_date', help='Transfection date', type=int, required=True)
    PARSER.add_argument('-t','--trans_plt', help='Transfection plate barcode', type=str, required=True)
    ARGS = PARSER.parse_args()
    #date & trafo plate barcode
    DATE = ARGS.trans_date
    TRANS_PLT = ARGS.trans_plt
 
    plasmid_ids = pd.read_excel(dir_plasmid_id)
    sorter = pd.read_excel(dir_sorter)
    plasmid_ids = sort_categorically(plasmid_ids,sorter.sorterA1_A2, 'PlateWell_WorkingStock',WS_col_sort ) #sort by transfection raster
    plasmid_ids.Working_Stock_ID.to_excel(os.path.join(dir_ass_imports, 'Ab_2_Import.xlsx'), index=False)#import for assignment table
    plasmid_ids = transpose_WS(plasmid_ids,WS_to_drop,WS_reshaped) #reshape to transfection-suitable
    plasmid_ids = plasmid_ids.drop(columns='Well_2') #drop not necessary
    plasmid_ids = add_date_barcode(plasmid_ids,'Transfection_date',DATE,'Transfection_Barcode',TRANS_PLT) #add remaining
    plasmid_ids.to_excel(os.path.join(dir_ab1_output,'Traf_import_{0}.xlsx'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))),index=False)