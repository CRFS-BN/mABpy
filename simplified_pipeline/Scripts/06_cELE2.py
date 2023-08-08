'''
WF parts: cELE parsing (output: cele parsed partial import files)

Author: Malwina Kotowicz
E-mail: malwina.kotowicz@dzne.de
'''
import pandas as pd
import os
import glob
from datetime import datetime

from config import (all_partial_imports, dir_cele, dir_output_cele, 
cols_peak, cele_cols_keep, cele_col_renamed, treshold_upper_bp, treshold_lower_bp, cele_to_drop_cols)

def add_cele_band(df, cele_well_col, ladder_well, decision_col):
    """ 
    Assigns Y when cele band present, N when no band present, n.a. when ladder well & cleans up DQN peak table results
    Input: decision_col -- col name where decision should be output
    
    """  
    
    no_band = df['Sample ID'].isnull()
    yes_band = df['Sample ID'].notna()
    na_band = df[cele_well_col] == ladder_well

    df.loc[yes_band, decision_col] = 'Y'
    df.loc[no_band, decision_col] = 'N'
    df.loc[na_band, decision_col] = 'n.a.'
    
    #change peak table DQN values to n.a. (readability purposes)
    assign_na_DQN = (df['DQN'] == 'N/A (Size threshold is less than lower marker end point)')
    df.loc[assign_na_DQN, 'DQN'] = 'n.a.'
    
    return df


def get_peakTable(cele_barcode, dir_cele):
    """ 
    Gets dir of peak table (in cele_barcode folder)
    Input: dir_cele -- peak tables directory, here 'CapillaryElectrophoresis'
    
    """
    dir_cele_barcode = os.path.join(dir_cele, cele_barcode.lower()) #folders cele
    dir_peak = glob.glob(os.path.join(dir_cele_barcode, '*Peak Table.csv'))[0] #indexing 0th element, cuz glob returns list with 1 element

    return dir_peak

def transform_peakTable(df, cele_well_col, cele_barcode_col, barcode_val,treshold_lower, treshold_upper): ### add tresholds!
    
    """ 
    Drops A1 ladder well, removes bands < treshold_lower, >treshold_upper bp, if two bands, drops the band with higher RFU
    
    Input: cele_well_col, cele_well_barcode are peak table col names where well, barcode. barcode_val is barcode value
    tresholds: lower -- min bp band size, upper -- max bp band size (int)
    """
    
    
    index_to_remove_a1 = df[df['Sample ID'] == 'SampA1'].index #get A1 well (ladder) index 
    df.drop(index_to_remove_a1, inplace=True) #drop A1 well samples
    
    index_to_remove_bp = df[(df['Size (bp)'] < treshold_lower) | (df['Size (bp)'] > treshold_upper)].index #get index of samples lower than 300 & bigger than 700 bp
    df.drop(index_to_remove_bp, inplace=True)#drop these
    
    df.sort_values(by=['Well','RFU'], inplace=True) #sort first by Well, then by RFU (ascending) to drop lower RFU value
    df.drop_duplicates(keep='last',subset='Well', inplace=True) #values sorted in ascending order, so keep='last' (higher RFU band)
    
    df[cele_barcode_col] = barcode_val
    df.rename(columns={'Well':cele_well_col}, inplace=True)#rename well 
    
    return df

if __name__ == '__main__':
    # create empty df with peak table cols
    df_peak_empty =  pd.DataFrame(columns=cols_peak)
    #get all output files from 05_PCR3
    partial_imports = sorted(glob.glob(all_partial_imports), key=os.path.getmtime)
    #get latest output file from 05_PCR3
    last_import = pd.read_excel(partial_imports[-1])

    for barcode in last_import.Cele_SpecPCR_Barcode.unique(): # for each cele barcode found in latest import
        dir_peak = get_peakTable(barcode, dir_cele)  #get peak table dir
        print('Barcode:',barcode, '\n', 'Directory:',dir_peak, '\n') #control prints
        df_peak_table = pd.read_csv(dir_peak)
        #drop samples not meeting criteria
        df_peak_table = transform_peakTable(df_peak_table, 'Cele_SpecPCR_Well', 'Cele_SpecPCR_Barcode', barcode, treshold_lower_bp, treshold_upper_bp)
        df_peak_empty = df_peak_empty.append(df_peak_table) #append to empty peak table template (best way so far)
    #merge with latest import file on cele barcode & well    
    last_import = last_import.merge(df_peak_empty,how='left',on=['Cele_SpecPCR_Barcode','Cele_SpecPCR_Well'])

    #add y,n,n.a. depending on cele results
    last_import = add_cele_band(last_import, 'Cele_SpecPCR_Well', 'A1', 'Decision_Cele_SpecPCR')
    #rename cols to import-suitable
    for col_old,col_new in zip(cele_cols_keep,cele_col_renamed):
        last_import = last_import.rename(columns={col_old:col_new})
    #add decision date column
    last_import.loc[:, 'Decision_Date'] = datetime.now().strftime('%Y%m%d')
    #drop not needed
    last_import.drop(cele_to_drop_cols, axis = 1, inplace=True)
    last_import.to_excel(os.path.join(dir_output_cele,'cele2_Intermed_{0}.xlsx'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))),index=False)