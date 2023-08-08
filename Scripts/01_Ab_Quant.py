import pandas as pd
import numpy as np
import os
from datetime import datetime
from config import (dir_assign_id, dir_trans_export, trans_cols_reshaped, dir_ab2_3_output,
                    dir_ass_updates, assign_cols, dir_htrf, dir_tubes_bonn, dir_tubes_berlin, drop_tube_cols,
                    tubes_col_names, dir_sorter, htrf_cols_drop, htrf_after_reshape, locations, 
                    transfection_method, harvest_columns)
from utils.plt_manipulators import drop_rename, reshape_to_wide
from utils.sorters import sort_categorically
import warnings

def trans_reshape(df, col_insert_value, col_insert_name, position, trans_cols_reshaped):
    """Duplicate trafo_id col and insert in position, needed for reshaping.
    Reshape based on factor (num of cols/2). reshaped col names = trans_cols_reshaped
    
    """
    df.insert(position,col_insert_name,df[col_insert_value])
    factor = int(len(df.columns)/2)
    trans_reshaped = pd.DataFrame(np.reshape(df.values,(-1,factor)), columns=trans_cols_reshaped)
    return trans_reshaped

def get_tube_position(df,col_position, tube_row, tube_col):
    """Concatenates tube row and col from raw tubescan file
    """
    df[col_position] = df[tube_row] + df[tube_col].astype(str)
    return df

def add_harvest_info(df, h_date, h_day, transfection_method):#modify funct, kinda hardcoded
    """Adds harvest info to df: date, harvest day and transfection method"""
    
    df['Harvest_Day'] = h_day
    df['Harvest_Date'] = h_date
    df['Transfection_Method'] = transfection_method #everywhere the same for now, later two options, auto taken   
    return df

def add_tube_info(df, location, volume): #modify funct, kinda hardcoded
    """Adds tube info: volume and location"""
    
    df['Location'] = location
    df['Volume_uL'] = volume
    return df

if __name__ == '__main__':

    #silence future warning 
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)

    assign_id = pd.read_excel(dir_assign_id)#get current assignment_ids
    trans_export_well = pd.read_excel(dir_trans_export)#get current trans_export
    trans_export = trans_export_well.drop(columns='Transfection_Well') #not needed for Ab_2_Update file

    #duplicate transf_id col in pos 3 (needed for reshaping), reshape using trans_cols_reshaped col names
    trans_reshaped = trans_reshape(trans_export,'Transfection_ID','Transfection_ID2',3,trans_cols_reshaped)
    assign_id = assign_id.merge(trans_reshaped,how='left',left_on = 'FK_Plasmid_WorkingStock_ID', right_on='pDNA_ID')#merge on pDNA to get transf_id
    assign_id[assign_cols].to_excel(os.path.join(dir_ass_updates, 'Ab_2_Update.xlsx'), index=False)#excerpt saved, PlasmidName_pDNA is for human supervision!

    htrf = pd.read_excel(dir_htrf)#read htrf file
    sorter = pd.read_excel(dir_sorter)

    htrf.drop(columns=htrf_cols_drop, inplace=True)#drop redundand htrf cols
    htrf = sort_categorically(htrf,sorter.sorterA1_A2, '96well', ['96well','plate'])#sort A1 raster & plt (needed for reshaping)
    htrf = reshape_to_wide(htrf, htrf_after_reshape) #reshape
    htrf['HTRF_Avg ug_mL'] =  htrf[['HTRF1 ug_mL', 'HTRF2 ug_mL']].mean(axis=1)#calculate avg

    #merge harvest with transf export on 96well,valid for 96 format
    new_merged = htrf.merge(trans_export_well, how='left', right_on='Transfection_Well', left_on='96well')

    locations = locations #internal LAT, external Berlin (subject to change)
    filepaths = [dir_tubes_bonn, dir_tubes_berlin] #raw tube scan files, per location
    harvest_empty_df = pd.DataFrame(columns=harvest_columns) #empty df, for appending 
    h_date = input('Enter harvest date YYYYMMDD...\n')
    h_day = input('Enter harvest day (e.g. D4)...\n').upper()

    #for each location, each tube scan raw file...
    for filepath, location in zip(filepaths, locations):
        volume = input('Enter the volume for {0} aliquot [ul]...\n'.format(location))
        tubes = pd.read_excel(filepath)#read tube files
        tubes = get_tube_position(tubes,'Aliquot_well', 'Tube Row', 'Tube Column') #get rack position
        tubes = drop_rename(tubes, drop_tube_cols, tubes_col_names) #drop not needed, rename
        tubes = add_tube_info(tubes,location,volume) #vol per location and location
        if location != 'LAT':
            tubes['Sent_Date_to_External'] = input('Enter date of sending to {0}...\n'.format(location))
        #merge with htrf, transf file (identical for each location) -> provides Trafo_ID and htrf results
        tubes = tubes.merge(new_merged,how='left', right_on='Transfection_Well', left_on='Aliquot_well')
        harvest_empty_df = harvest_empty_df.append(tubes)#append all to empty df (for each location)

    harvest_empty_df = add_harvest_info(harvest_empty_df, h_date, h_day, transfection_method) #adds harvest date, day and transf method
    #getting final excerpt for harv import table
    harvest_empty_df = harvest_empty_df[harvest_columns]
    harvest_empty_df.to_excel(os.path.join(dir_ab2_3_output,'HarvestHTRF_import_{0}.xlsx'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))), index=False) #save import file