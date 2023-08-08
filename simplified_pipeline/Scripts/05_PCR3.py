'''
WF parts: specPCR to cELE (output: new store list, echo spotting lists, partial import files)

Author: Malwina Kotowicz
E-mail: malwina.kotowicz@dzne.de
'''

import pandas as pd
import os
from datetime import datetime
import glob
from config import (dir_primer_lookup, dir_store, all_store_lists, dir_sorter, template_vol,primer_vol, 
                    dir_output, dir_partial_imports, cols_tspotting, renamed_cols_spotting, cols_specPCR_import, 
                    cols_pspotting,dir_knime_baseid,baseid_drop,dir_old_baseid, chunk_96)
from utils.plt_manipulators import  (split_specPCR, get_specPCR_list, get_plt_numbers, get_pcr3, get_wells, split_into_chunks)
from utils.spotting_lists import get_tspotting_list
import argparse
import shutil

def specPCR_list_processing(df,specpcr_barcode, specpcr_well, cols_specPCR_import, import_file,
                           cele_barcode,copy_barcode,copy_well):

    """ Adds vals to 'SpecPCR_Barcode' & 'SpecPCR_Well' to df (specPCR_list). 
    Excerpt df by cols_specPCR_import is now part of db import file (for this chunk)

    """
    
    df.loc[:, 'SpecPCR_Barcode']= specpcr_barcode
    df.loc[:, 'SpecPCR_Well'] = specpcr_well
    df.loc[:, 'SpecPCR_copy_Barcode'] = copy_barcode
    df.loc[:, 'SpecPCR_copy_Well'] = copy_well
    df.loc[:, 'Cele_SpecPCR_Barcode'] = cele_barcode
    df.loc[:, 'Cele_SpecPCR_Well'] = specpcr_well
    #import file gets exerpt from df appended
    import_file = import_file.append(df[cols_specPCR_import])
    

    return df,import_file

def get_primer_vals(df,_5primer_col,_3primer_col):
    
    """ Gets primer values by stacking 5' primer with 3' primer from specPCR list 
    
    """
    
    primer_values = df[_5primer_col].append(df[_3primer_col])
    #reset index and drop an old one, otherwise pandas complains later on
    primer_values.reset_index(drop=True, inplace=True)
    
    return primer_values


def get_pspotting_list(cols, primer_plate_barcode, primer_values, specpcr_barcode, specpcr_well, primer_vol):
    
    """ Gets primer spotting lists, echo suitable. Cols order must remain
    """
    pspotting = pd.DataFrame(columns=cols)
    pspotting['Primer'] = primer_values
    pspotting['Destination Well'] = specpcr_well
    pspotting['Destination Plate Barcode'] = specpcr_barcode
    pspotting['Source Plate Barcode'] = primer_plate_barcode
    pspotting['Volume'] = primer_vol
    
    return pspotting

def get_source_well(df,df_reference, col_to_merge_on, final_pos):
        
    """ Gets well for specPCR primer from lookup table, reinserts it into final_pos in df
    
    """
    #merge primer lookup table with primer cherry pick list on primer col., df gets source well col
    pspotting = pd.merge(df, df_reference,  how='left', on=[col_to_merge_on])
    
    #cols order echo-suitable, pop source well col 
    col = pspotting.pop('Source Well')
    #and now insert it again in final_pos
    pspotting.insert(final_pos, col.name, col)
    
    return pspotting

if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-s','--specPCRplate', help='Latest specPCR plate number', type=int, required=True)
    PARSER.add_argument('-e','--cele_plate', help='Latest cele plate number', type=int, required=True)
    PARSER.add_argument('-c','--specPCR_COPY_plate', help='Latest specPCR copy plate number', type=int, required=True)
    ARGS = PARSER.parse_args()
    #last specPCR plt num
    LAST_SPECPCR_PLATE = ARGS.specPCRplate
    LAST_CELE_PLATE = ARGS.cele_plate
    LAST_COPY_PLATE = ARGS.specPCR_COPY_plate

    #silence SettingWithCopyError
    pd.options.mode.chained_assignment = None  # default='warn'

    #read Primer lookup file 
    primer_lookup = pd.read_excel(dir_primer_lookup)

    #sorter
    sorter = pd.read_excel(dir_sorter)

    #sort store lists by creation date
    store_lists = sorted(glob.glob(all_store_lists), key=os.path.getmtime)

    #get latest store list
    current_store_list = pd.read_excel(store_lists[-1])

    #copy current baseid dict with timestamp, before tinkering 
    shutil.copy(dir_knime_baseid, os.path.join(dir_old_baseid, '{0}_ID_Dictionary.xlsx'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))))
    #for merging, get aBASE_IDs
    baseid = pd.read_excel(dir_knime_baseid)
    #melt to get vals of seq_name per chain (needed for merging)
    baseid = pd.melt(baseid, id_vars=['aBASE_ID'], value_vars=['Seq1_Name_heavy','Seq1_Name_kappa','Seq1_Name_Lambda'], value_name='Seq1_Name')

    floor_specPCR, modulo_specPCR = split_specPCR(current_store_list, chunk_96) #floor (no. of 96 well plates) & modulo (samples to remain)
    print('Total no. of samples for specPCR now: ', len(current_store_list), '\nNo. of specPCR plates: ', floor_specPCR, '\nNo. of samples to remain: ',modulo_specPCR)

    #last N samples = final store list
    final_store_list = current_store_list.tail(modulo_specPCR)
    if floor_specPCR != 0:
        final_store_list.to_excel(os.path.join(dir_store,'PCR3_StoreList_{0}.xlsx'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))),index=False)
        print('\nStore list saved at {0} in dir {1}'.format(datetime.now().strftime('%Y%m%d-%H%M%S'),dir_store ))
    else: 
        print('\nNo new store list saved.')

    #ARGS: LAST specPCR PLT number, number of plates is floorspecPCR
    plate_numbers = get_plt_numbers(LAST_SPECPCR_PLATE,floor_specPCR)
    #ARGS: LAST cele PLT number, number of plates is floorspecPCR
    cele_plates =  get_plt_numbers(LAST_CELE_PLATE,floor_specPCR)
    ##ARGS: LAST specPCR COPY PLT number, number of plates is floorspecPCR
    copy_plts = get_pcr3(LAST_COPY_PLATE,floor_specPCR)
    #specPCR copy plate wells
    copy_wells = get_wells(floor_specPCR,sorter.sorterA1_A3,sorter.sorterA2_A4)

    #merge to get aBASE IDs, merging on seq_name (unique)
    current_store_list = current_store_list.merge(baseid, how='left', on = 'Seq1_Name')
    # drop cols used for merge, keep aBASE_ID
    current_store_list.drop(columns=baseid_drop, inplace=True)

    #get samples for this specPCR round
    specPCR_list = get_specPCR_list(current_store_list,final_store_list)

    import_file = pd.DataFrame(columns=cols_specPCR_import) #partial import file

    for i in range(floor_specPCR): #for each specPCR plate (floor_specPCR)...
        #split specPCR list into no. of specPCR plates and index split parts (first, middle, last)
        specPCR_list_split = split_into_chunks(specPCR_list,floor_specPCR,i)
        
        #append specPCR barcode & well, get partial import file (concat all iterations)
        specPCR_list_split, import_file = specPCR_list_processing(specPCR_list_split,'BAOsPCR3p{0}'.format(plate_numbers[i]), sorter.sorterA1_A2.values, cols_specPCR_import, import_file,
                                                                'BAOsCELEp{0}'.format(cele_plates[i]),'BAOsP3COp{0}'.format(copy_plts[i]),copy_wells[i])
        
        #get template spotting list as excerpt of specPCR_list_split + vol
        tspotting = get_tspotting_list(specPCR_list_split,cols_tspotting, renamed_cols_spotting,template_vol)
        tspotting.to_csv(os.path.join(dir_output, 'BAOsPCR3p{0}_TemplatePickList.csv'.format(plate_numbers[i])), index=False)

        #get primer vals
        primer_values = get_primer_vals(specPCR_list_split, "Primer 5'", "Primer 3'" )
        pspotting_well = pd.concat([sorter.sorterA1_A2]*2, ignore_index=True) #destination well = sorter, doubled

        #get primer spotting lists
        pspotting = get_pspotting_list(cols_pspotting,'PrimerPlate', primer_values,'BAOsPCR3p{0}'.format(plate_numbers[i]), pspotting_well, primer_vol)
        #merge primer lookup table with primer cherry pick list on primer col., df gets source well col
        pspotting = get_source_well(pspotting,primer_lookup, 'Primer', 1)
        
        #save as .csv (primer pick list in 5_SpecPCR)
        pspotting.to_csv(os.path.join(dir_output, 'BAOsPCR3p{0}_PrimerPickList.csv'.format(plate_numbers[i])), index=False)

    #save import file for all plates to specPCR if not empty
    if len(import_file.index) != 0:
        import_file.to_excel(os.path.join(dir_partial_imports, 'PCR3_Intermed_{0}.xlsx'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))), index=False)