'''
WF parts: Gibson Assembly spotting lists

Author: Malwina Kotowicz
E-mail: malwina.kotowicz@dzne.de
'''
import pandas as pd
import numpy as np
import os
from datetime import datetime
import glob

from config import (all_cele_parsed, dir_output_gias, dir_import_gias, gias_pcr3_cols, pcr_prod_vol,
                    plasmid_vol, renamed_cols_spotting, mm_vol, mm_plt_name, plasmid_plt_name, gias_plasmid_excerpt_cols, 
                    echo_spotting_cols, chain_letters, dir_sorter)

from utils.plt_manipulators import get_plt_numbers, split_into_chunks, repeat_raster
from utils.spotting_lists import get_tspotting_list

import argparse

def pair_plts_and_wells(df, ref_col, ref_col_val, dest_col, dest_col_val, dest_col2, dest_col2_val ):
    """Used to add new col barcode value into df, based on val in another col, already present in df

    ref_col is col name of reference col in df, ref_col_val is a conditional val in this column,
    dest_col is col name of barcode destination col, dest_col_val is a value in barcode column

    dest_col2 is a col name of well destination col, dest_col2_val is a value in well column 
    """

    df.loc[df[ref_col] == ref_col_val , dest_col] = dest_col_val
    df.loc[:, dest_col2] = dest_col2_val

    return df

def get_pla_mm_spotting(df_ref, col_names, vol, source_plt_name):
    """Gets pla spotting lists, by getting excerpt of df_ref (here destination col, well, chain) valid for
    mm and plasmid gibson plates, source_plt_name is 'Source Plate Well' in final spotting list """

    df = df_ref[col_names] 
    df.loc[:, 'Volume'] = vol
    df.loc[:, 'Source Plate Barcode'] = source_plt_name
    
    return df

def get_plasmid_well(df, wells_plasmid, letters):
    """ Assigns plasmid well based on wells_plasmid vals. These must correspond to chains letter names in letters
    """
    for well, letter in zip(wells_plasmid,letters):
    
        df.loc[(df['chain']==letter), 'Source Well'] = well
        
    return df

def get_mm_well(df,mm_wels):
    """Gets master mix wells, vol in one well sufficient for 32 destination wells, for 96 well plt 3xPP well """
    
    df.insert(0,'Source Well','')
    df['Source Well'][:32] = mm_wels[0]
    df['Source Well'][32:64] = mm_wels[1]
    df['Source Well'][64:] = mm_wels[2]
    
    return df

if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-g','--gibson_plt', help='Latest gibson plate number', type=int, required=True)
    ARGS = PARSER.parse_args()
    LAST_GIAS_PLATE = ARGS.gibson_plt

    #silence SettingWithCopyError
    pd.options.mode.chained_assignment = None  # default='warn'

    sorter = pd.read_excel(dir_sorter) #needed for Gibson well

    #get all output files from 06_cELE
    cele_parsed = sorted(glob.glob(all_cele_parsed), key=os.path.getmtime)
    #get latest output file from WF5
    last_cele = pd.read_excel(cele_parsed[-1])

    #get specPCR plts in last cele (used to match with gias barcode)
    specPCR_plts = last_cele.SpecPCR_Barcode.unique()
    #get gias plts based on last gias plt in args
    gias_plts = get_plt_numbers(LAST_GIAS_PLATE,len(specPCR_plts))

    #get gibson wells, repeats A1_A3 raster to fit last_cele len
    gias_well = repeat_raster(sorter.sorterA1_A3, last_cele)

    for gias_plt, specPCR_plt in zip(gias_plts, specPCR_plts): #getting the final import for WF4 to WF6
    
        #wherever specPCR barcode == specPCR_plt, GiAS_Barcode == gias_plt; GiAS_Well == repeated A1_A3 raster
        last_cele = pair_plts_and_wells(last_cele, 'SpecPCR_Barcode', specPCR_plt, 'GiAS_Barcode', 'BAOsGiAsp{0}'.format(gias_plt), 'GiAS_Well', gias_well)
    #save as import when all gias plts paired    
    last_cele.to_excel(os.path.join(dir_import_gias,'GiAS_import_{0}.xlsx').format(datetime.now().strftime('%Y%m%d-%H%M%S')), index=False)

    #excerpt with cols for pcr3 product spotting
    pcr_product_all = get_tspotting_list(last_cele, gias_pcr3_cols, renamed_cols_spotting, pcr_prod_vol)

    #chunks of 96 samples
    chunks = int((len(pcr_product_all)/96))
    print('Number of Gibson Plates: ', chunks) #let user know how many times input requested...

    #in range of number of gias plts...
    for i in range(chunks):

        gibson_samples_now = split_into_chunks(pcr_product_all,chunks,i) #current samples to gias = all samples splt in chunks, indexing first, middle(s), last chunks
        
        wells_plasmid = input('Enter heavy, kappa, lambda plasmid wells, separated by comma for plate {}...\n'.format(i+1)).split(',')
        #get mm spotting with cols for gias excerpt, use pla vol and plt name
        plasmid_spotting = get_pla_mm_spotting(gibson_samples_now,gias_plasmid_excerpt_cols,plasmid_vol,plasmid_plt_name)  
        plasmid_spotting = get_plasmid_well(plasmid_spotting, wells_plasmid, chain_letters) #wells where each chain
        plasmid_spotting = plasmid_spotting.reindex(echo_spotting_cols,axis=1)#better readability

        wells_mm = input('Enter MM wells, separated by comma for plate {}...\n'.format(i+1)).split(',')
        #get mm spotting with cols for gias excerpt, use mm vol and plt name
        mm_spotting = get_pla_mm_spotting(gibson_samples_now,gias_plasmid_excerpt_cols,mm_vol,mm_plt_name)
        mm_spotting = get_mm_well(mm_spotting,wells_mm) #3 wells with mm
        mm_spotting = mm_spotting.reindex(echo_spotting_cols,axis=1) #better readability
        
        #drop chain before saving pcr prod
        gibson_samples_now.drop(columns=['chain']).to_csv(os.path.join(dir_output_gias,'{0}_PCR_Spotting.csv').format(gibson_samples_now['Destination Plate Barcode'].unique()[0]), index=False) #indexing 0, otherwise brackets in filename
        plasmid_spotting.to_csv(os.path.join(dir_output_gias,'{0}_Pla_Spotting.csv').format(gibson_samples_now['Destination Plate Barcode'].unique()[0]), index=False)
        mm_spotting.to_csv(os.path.join(dir_output_gias,'{0}_MM_Spotting.csv').format(gibson_samples_now['Destination Plate Barcode'].unique()[0]), index=False)