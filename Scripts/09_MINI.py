'''
Picking to minipreps handlers

Author: Malwina Kotowicz
E-mail: malwina.kotowicz@dzne.de
'''
import pandas as pd
from config import dir_trfo_id, all_plating, dir_sorter, dir_output_minis
from utils.microbiology_supporters import insert_growth_cultureplate2, add_barcodes
from utils.sorters import unique_non_null
import glob
import os
from datetime import datetime

def fill_missing_vals(df, cul_barcode, cul_well):
    """Fill nans in culture plt barcode (empty due to no colonies picked). Backward fill if A1, forward fill otherwise"""
    where_A1 = (df[cul_well] == 'A1')
    where_no_A1 = (df[cul_well] != 'A1')

    df.loc[where_A1, cul_barcode] = df[cul_barcode].fillna(method='bfill')
    df.loc[where_no_A1, cul_barcode] = df[cul_barcode].fillna(method='ffill')
    return df

def add_repick_mini_date(df,cul_barcode,repick, date):
    """Add info on whether repick & minipreps date
    """
    condition = df['CulturePlate1_Barcode'] == cul_barcode
    df.loc[condition, 'Repick'] = repick
    df.loc[condition, 'MiniPrepDate'] = date
    return df

def get_nanodrops(nanodrop_list):
    """Gets dictionary with wells and concentrations
    """
    item = iter(nanodrop_list)
    nanodrop_dict = dict(zip(item, item))
    return nanodrop_dict
         
def add_conc(df, cul_barcode, conc_col, nanodrop_values):
    """Ads nanodrop concentration to respective wells
    """

    for key, value in nanodrop_values.items():
        condition = (df['CulturePlate1_Barcode'] == cul_barcode) & (df['PLA1_Well'] == key.upper())
        df.loc[condition, conc_col] = value
    
    return df

if __name__ == '__main__':
    #get trfo ids
    trfo_id = pd.read_excel(dir_trfo_id)

    #get last partial import (assuming last trfo is considered for plating, must modify if not)
    last_trfos = sorted(glob.glob(all_plating), key=os.path.getmtime)#modification time
    last_trfo_import = pd.read_excel(last_trfos[-1])#latest

    sorter = pd.read_excel(dir_sorter)

    last_trfo_import = last_trfo_import.merge(trfo_id, how='left',on=['Qtray_Barcode','Qtray_well'])
    last_trfo_import = fill_missing_vals(last_trfo_import, 'CulturePlate1_Barcode', 'CulturePlate1_Well')

    barcodes = unique_non_null(last_trfo_import.CulturePlate1_Barcode)
    for cul_barcode in barcodes:
        
        gly_now = input('Enter GLYCEROL stock barcode for culture plate {0}...\n'.format(cul_barcode))
        pla_now = input('Enter PLASMID plate barcode for culture plate {0}...\n'.format(cul_barcode))
        wells_now = input('Enter WELLS with NO GROWHT for culture plate {0}, separated by commas...\n'.format(cul_barcode)).split(',')
        wells_now = [x.strip() for x in wells_now] #safety, if unwanted space in input
        date_mini = input('Enter MINIPREPS date for culture plate {0} as YYYYMMDD...'.format(cul_barcode))
        repick = input('Was culture plate {0} a REPICK? N if no, Y+repick num if yes e.g., Y1...\n'.format(cul_barcode)).upper()
        nanodrop_list = input('Enter WELLS + CONC for culture plate {0}, separated by commas, format: well,conc...\n'.format(cul_barcode)).split(',')
        nanodrop_list = [x.strip() for x in nanodrop_list] #safety, if unwanted space in input
        
        last_trfo_import = insert_growth_cultureplate2(last_trfo_import, cul_barcode, wells_now) #add no growth on culture plt
        last_trfo_import = add_barcodes(last_trfo_import,cul_barcode, gly_now, pla_now, sorter.sorterA1_A2.values)#add gly, pla plt and wells
        last_trfo_import = add_repick_mini_date(last_trfo_import,cul_barcode,repick,date_mini)#repick info and minipreps date
        nanodrop_list = get_nanodrops(nanodrop_list) #dict of wells + nanodrops conc
        last_trfo_import = add_conc(last_trfo_import,cul_barcode,'NANODROP_conc',nanodrop_list)#add conc to respective wells

    #save results
    last_trfo_import.to_excel(os.path.join(dir_output_minis,'MINI_import_{0}.xlsx'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))),index=False)