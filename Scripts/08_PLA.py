'''
Plating scripts

Author: Malwina Kotowicz
E-mail: malwina.kotowicz@dzne.de
'''
import pandas as pd
from config import (dir_plating, dir_gias_id, dir_picking, dir_sorter, cols_trfo, cols_pick, cols_mibi, 
                    cols_trafo_import, dir_partial_plating, dir_output_trfo)
from utils.sorters import sort_categorically
from utils.microbiology_supporters import insert_colonies
from datetime import datetime
import os
import warnings

def rename_add_gibson(df, cols_new, gibson_barcode):
    """Renames to cols_new, adds gibson barcode val
    """
    df.columns = cols_new
    df.loc[:, 'GiAS_Barcode'] = gibson_barcode
    
    return df

def clean_picking_df(df,cols_pick):
    """ Removes unecesarry cols, changes col names to cols_pick
    """
    df.drop(columns=['Feature Position X', 'Feature Position Y'], inplace=True)
    df.columns = cols_pick
    return df

if __name__ == '__main__':
    #silence future warning 
    warnings.simplefilter(action='ignore', category=FutureWarning)

    gibson_export = pd.read_excel(dir_gias_id) #read gibson with FK_IDs
    sorter = pd.read_excel(dir_sorter) #get sorters for cat sort

    print('Gibson barcodes in this transformation round...',[x for x in gibson_export.GiAS_Barcode.unique()])
    trfo_fnames = input('Enter trafo filenames, in Gibson order, separated by commas: \n').split(',')
    trfo_fnames = [x.strip() for x in trfo_fnames]#safety, if unwanted space in input
    pick_fnames = input('Enter picking filenames, in Gibson order, separated by commas: \n').split(',')
    pick_fnames = [x.strip() for x in pick_fnames]#safety, if unwanted space in input

    trfo_all = pd.DataFrame(columns=cols_mibi)#empty df with mibi cols

    for ftrfo,fpick,gibson_barcode in zip(trfo_fnames,pick_fnames,gibson_export.GiAS_Barcode.unique()): 
        
        trfo_current = pd.read_csv(os.path.join(dir_plating, ftrfo))#read corresponding plating & pick files
        pick_current = pd.read_csv(os.path.join(dir_picking, fpick))
        
        #important: adding gibson barcode now, so that later sort doesnt screw pairing of trafo-gibson barcodes
        trfo_current = rename_add_gibson(trfo_current,cols_trfo,gibson_barcode)
        trfo_current = sort_categorically(trfo_current, sorter.sorterA1_A2,'Trafo_Well', ['Trafo_Barcode','Trafo_Well'])#sort cuz adding corresponding gibson wells later
        
        pick_current = clean_picking_df(pick_current,cols_pick)
        
        trfo_current = trfo_current.merge(pick_current, how='left', on=['Qtray_Barcode','Qtray_well'])#these barcodes must match! settigs on qpix
        trfo_current.loc[:, 'GiAS_Well'] = sorter.sorterA1_A3 #adding gias wells at the end, for some reasons merging above screws raster
        
        trfo_all = trfo_all.append(trfo_current)#append all to empty template

    trfo_all = trfo_all.merge(gibson_export, how='left', on=['GiAS_Barcode', 'GiAS_Well'])#merge with gibson export to get FK_ID
    trfo_all = insert_colonies(trfo_all,'CulturePlate1_Well','Colonies')#add Y or N is colonies present on qtrays

    #save trafo import file & partial plating import
    trfo_all[cols_trafo_import].to_excel(os.path.join(dir_output_trfo, 'PLA_import_{0}.xlsx'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))),index=False)
    trfo_all[cols_pick].to_excel(os.path.join(dir_partial_plating, 'PICK_Intermed_{0}.xlsx'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))),index=False)