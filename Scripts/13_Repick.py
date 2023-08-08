'''
WF parts: repick lists

Author: Malwina Kotowicz
E-mail: malwina.kotowicz@dzne.de
'''

import pandas as pd
import os
from datetime import datetime
import glob
from config import (dir_full_repick_list, dir_repicks, dir_merged_for_doublecheck, dir_sorter, 
                    dir_repick_storelists, dir_manual_lists, all_repick_store, repick_cols_drop, repick_manual)

from utils.plt_manipulators import (split_specPCR, get_specPCR_list, get_plt_numbers, 
                                    split_into_chunks,insert_col_at_end)
from utils.microbiology_supporters import add_barcodes_repick
from utils.sorters import sort_categorically
import argparse

if __name__ == '__main__':
    
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-c','--culture_plate', help='Latest culture plate number', type=int, required=True)
    PARSER.add_argument('-b','--glycerol_stock_plate', help='Latest glycerol stock plate number', type=int, required=True)
    PARSER.add_argument('-p','--plasmid_plate', help='Latest plasmid plate number', type=int, required=True)
    ARGS = PARSER.parse_args()
    #last  plt num
    LAST_CULTURE_PLATE = ARGS.culture_plate
    LAST_GLYCEROL_PLATE = ARGS.glycerol_stock_plate
    LAST_PLASMID_PLATE = ARGS.plasmid_plate

    #silence SettingWithCopyError
    pd.options.mode.chained_assignment = None  # default='warn' 

    #sorter
    sorter = pd.read_excel(dir_sorter)

    # all repicks in db so far (used for merge)
    full_repick_list = pd.read_excel(dir_full_repick_list)

    #sort store lists by creation date
    repick_store = sorted(glob.glob(all_repick_store), key=os.path.getmtime)

    #get latest store list
    current_repick_store = pd.read_excel(repick_store[-1])

    floor_repick, modulo_repick = split_specPCR(current_repick_store, 96) #floor (no. of 96 well plates) & modulo (samples to remain)
    print('Total no. of samples for repick now: ', len(current_repick_store), '\nNo. of repick plates: ', floor_repick, '\nNo. of samples to remain: ',modulo_repick)

    #last N samples = final store list
    final_store_list = current_repick_store.tail(modulo_repick)
    if floor_repick != 0: #if 1 repick plt or more 
        final_store_list.to_excel(os.path.join(dir_repick_storelists,'Repick_StoreList_{0}.xlsx'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))),index=False) #new store list
        print('\nStore list saved at {0} in dir {1}'.format(datetime.now().strftime('%Y%m%d-%H%M%S'),dir_repick_storelists))
    else:
        print('\nNo new store list saved.')

    #ARGS: LAST cul PLT number, number of plates is floor_repick
    cul_plates = get_plt_numbers(LAST_CULTURE_PLATE,floor_repick)
    #ARGS: LAST bast PLT number, number of plates is floor_repick
    bast_plates =  get_plt_numbers(LAST_GLYCEROL_PLATE,floor_repick)
    #ARGS: LAST pla PLT number, number of plates is floor_repick
    pla_plates =  get_plt_numbers(LAST_PLASMID_PLATE,floor_repick)

    #get samples for this repick round
    repick_list = get_specPCR_list(current_repick_store,final_store_list)

    #merge with list of full repick to get gly plt to pick from 
    repick_list = repick_list.merge(full_repick_list, how='left', left_on='Plating_ID', right_on='FK_Plating_ID') #merge with list of all samples ever repicked (export from db) to get current GLY stocks
    repick_list.to_excel(os.path.join(dir_merged_for_doublecheck,'Repick_Intermed_{0}.xlsx'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))),index=False)#file for merge control check 

    for i in range(floor_repick): #for each repick plate (floor_repick)...
        #split repick list into no. of repicks plates and index split parts (first, middle, last)
        repick_list_split = split_into_chunks(repick_list,floor_repick,i)
        
        # copy current GLY stocks barcodes and well to new cols
        repick_list_split = insert_col_at_end(repick_list_split, 'BAST_PICK_BARCODE', repick_list_split['GlycerolStock_Barcode'].values)
        repick_list_split = insert_col_at_end(repick_list_split, 'BAST_PICK_WELL', repick_list_split['GlycerolStock_Well'].values)
        
        # add comment on sample origin (which GLY), added here due to converting BAST_WELL to cat later on
        repick_list_split['Comment'] = 'inoculated from/identical with ' + repick_list_split['BAST_PICK_BARCODE'] + ', ' + repick_list_split['BAST_PICK_WELL']
        
        #sort by current GLY and well, needed for manual manouvers
        repick_list_split = sort_categorically(repick_list_split, sorter.sorterA1_A2, 'BAST_PICK_WELL', ['BAST_PICK_BARCODE','BAST_PICK_WELL'])

        repick_list_split.reset_index(inplace=True, drop=True) #needed for correct well raster assignment later on...
        repick_list_split.drop(columns=repick_cols_drop, inplace=True) #drop unnecesarry cols 
        #add new cul, pla, gly barcodes + wells
        repick_list_split = add_barcodes_repick(repick_list_split, 'BAOsCUL1p{0}'.format(cul_plates[i]), 'BAOsBASTp{0}'.format(bast_plates[i]), 'BAOsPLA1p{0}'.format(pla_plates[i]), sorter.sorterA1_A2)
        #preps date
        repick_list_split['MiniPrepDate'] = input('Enter miniprep date for plate {0} '.format('BAOsCUL1p{0}'.format(cul_plates[i])))
        #save a list for manual repick, wet-lab handling 
        manual_pick = repick_list_split[repick_manual]
        
        if len(repick_list_split.index) != 0: #if anything on repick list...
            repick_list_split.to_excel(os.path.join(dir_repicks, 'Repick_Import_{0}.xlsx'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))), index=False)#save import list
            manual_pick.to_excel(os.path.join(dir_manual_lists, 'Manual_Repicks_{0}.xlsx'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))), index=False)#save manual picking file