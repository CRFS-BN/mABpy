
'''
Default config variables which maybe overridden by a user config.

Author: Malwina Kotowicz
E-mail: malwina.kotowicz@dzne.de
'''
import os
# =================================
# PATHS general
# =================================
dir_parent = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) # get absolute path, os independent of parent dir of current working dir
dir_grandparent = os.path.abspath(os.path.join(dir_parent, os.pardir)) #get grandparnt abs path
dir_store = os.path.join(dir_parent,'PCR3_Store_Lists') 
dir_input = os.path.join(dir_parent,'Input') 
dir_output = os.path.join(dir_parent,'05_PCR3_Out') 
dir_partial_imports  = os.path.join(dir_output,'Intermed_Files')
dir_output_cele = os.path.join(dir_parent,'06_cELE2_Out') 
dir_output_trfo = os.path.join(dir_parent,'08_PLA_Out') 
dir_output_minis = os.path.join(dir_parent,'09_MINI_Out') 
dir_output_gias = os.path.join(dir_parent,'07_GiAS_Out') 
dir_import_gias = os.path.join(dir_output_gias, '07_GiAS_imports')
dir_ab1_output = os.path.join(dir_parent,'00_Ab_Traf_Out')
dir_ass_imports = os.path.join(dir_ab1_output,'DB_join_table')
dir_ab2_3_output = os.path.join(dir_parent,'01_Ab_Quant_Out')
dir_ass_updates = os.path.join(dir_ab2_3_output,'DB_join_table') 
dir_repicks = os.path.join(dir_parent,'13_Repicks_Out')
dir_repick_storelists = os.path.join(dir_repicks,'Store_Lists')
dir_merged_for_doublecheck = os.path.join(dir_repicks,'Intermed_Files')
dir_manual_lists = os.path.join(dir_repicks,'Manual_Repicks')
#plate grids
dir_sorter = os.path.join(dir_input,'sorter.xlsx')
# =================================
# PATHS cele
# =================================
#experimental redouts dir
dir_experimental = os.path.join(dir_parent, 'Experimental_Data')
#cele results
dir_cele = os.path.join(dir_experimental, 'cELE')
all_cele_parsed = os.path.join(dir_output_cele, '*.xlsx') #all cele2 output files (.xlsx)
# =================================
# PATHS Input files
# =================================
dir_gias_id = os.path.join(dir_input,'Gibson_IDs.xlsx')#get FK_IDs from specPCR_to_Gias
dir_trfo_id = os.path.join(dir_input,'Trfo_IDs.xlsx')#get FK_IDs from trfo
dir_knime_baseid = os.path.join(dir_parent,'04_Parse_Out', 'ID_Dictionary', 'ID_Dictionary.xlsx') #get dir baseids
dir_old_baseid = os.path.join(dir_parent,'04_Parse_Out', 'ID_Dictionary', 'old_files') #get dir baseids
dir_plasmid_id = os.path.join(dir_input,'Plasmid_IDs.xlsx')#get FK_IDs from plasmids
dir_assign_id = os.path.join(dir_input,'Assign_ID.xlsx')#get FK_IDs from assignment
dir_trans_export = os.path.join(dir_input,'Trans_Export.xlsx')#get FK_IDs from assignment
dir_htrf = os.path.join(dir_input,'HTRF.xlsx')#get HTRF file
dir_tubes_bonn = os.path.join(dir_input,'Tubes_Bonn.xls') #get tubes for bonn rack
dir_tubes_berlin = os.path.join(dir_input,'Tubes_Berlin.xls') #get tubes for berlin rack
dir_full_repick_list = os.path.join(dir_input,'Repick_Full_List.xlsx') #get all repicks in db so far
# =================================
# PATHS MiBi
# =================================
# dir qpix files
dir_plating = os.path.join(dir_experimental, 'qpix', 'plating')
dir_picking = os.path.join(dir_experimental, 'qpix', 'picking')
#partial files with culture plates, to be merged with FK_ID from trafo
dir_partial_plating = os.path.join(dir_output_trfo,'Intermed_Files')
#all plating files
all_plating = os.path.join(dir_partial_plating, '*.xlsx')
# =================================
# PATHS specPCR
# =================================
#all xlsx files in partial imports after specPCR
all_partial_imports = os.path.join(dir_partial_imports, '*.xlsx')
#PCR3 primer file
dir_primer_lookup = os.path.join(dir_input,'PCR3_primer.xlsx')
#get all xlsx files in dir_store
all_store_lists = os.path.join(dir_store, '*.xlsx')

# =================================
# PATHS repicks
# =================================
## all xlsx files in repick store list dir
all_repick_store = os.path.join(dir_repick_storelists, '*.xlsx') 

# =================================
# specPCR
# =================================
chunk_96 = 96 #96 samples processed at once

baseid_drop = ['_2_PCR_to_CELE_S::PCR_to_CELE_ID','variable'] #cols to drop when merging with baseid

# volume for specPCR template spotting
template_vol = 1800

# vol for primer spotting
primer_vol = 250

# store list excerpt cols for specPCR template spotting
cols_tspotting = ['PCR1_copy_Barcode',
       'PCR1_copy_Well','SpecPCR_Barcode', 'SpecPCR_Well']

#  cols for specPCR template spotting, echo compatibile
renamed_cols_spotting = ['Source Plate Barcode',
       'Source Well','Destination Plate Barcode', 'Destination Well']

#cols for partial import file
cols_specPCR_import = ['aBASE_ID', 'chain', 'SpecPCR_Barcode', 'SpecPCR_Well', 'SpecPCR_copy_Barcode', 'SpecPCR_copy_Well',	'Cele_SpecPCR_Barcode','Cele_SpecPCR_Well']

#cols for specPCR primer spotting, echo compatibile
cols_pspotting = ['Source Plate Barcode', 'Destination Plate Barcode','Destination Well', 'Volume', 'Primer']

# =================================
# capillary electrophoresis
# =================================

#config peak table columns
cols_peak = ['Cele_SpecPCR_Well', 'Sample ID', 'ng/ul', 'Size (bp)',
       '% (Conc.) (ng/uL)', 'nmole/L', 'RFU', 'TIC (ng/ul)', 'TIM (nmole/L)',
       'Total Conc. (ng/ul)', 'DQN', 'Threshold', 'Cele_SpecPCR_Barcode']
#peak table cols to keep for imports
cele_cols_keep = ['RFU','Size (bp)','% (Conc.) (ng/uL)','DQN', 'Total Conc. (ng/ul)']
#renamed peak table cols to keep for imports
cele_col_renamed = ['RFU_Cele_SpecPCR','BP_Cele_SpecPCR', 'ProcConc_Cele_SpecPCR','DQN_Cele_SpecPCR', 'TotalConc_Cele_SpecPCR']
#not needed for imports
cele_to_drop_cols = ['Sample ID', 'ng/ul', 'nmole/L', 'TIC (ng/ul)', 'TIM (nmole/L)',
                  'Threshold']
#cele bp band tresholds for specpcr cele 
treshold_upper_bp = 700
treshold_lower_bp = 300

# =================================
# gibson assembly 
# =================================
# needed for pcr product spotting
gias_pcr3_cols = ['SpecPCR_copy_Barcode','SpecPCR_copy_Well', 'GiAS_Barcode', 'GiAS_Well', 'chain']
pcr_prod_vol = 350
plasmid_vol = 650
mm_vol = 1000
mm_plt_name = 'PP_BP_MasterMix' #arbitrary master mix plt name (spotting)
plasmid_plt_name = 'PP_SP_Pla' #arbitrary plasmid plt name (spotting)
# get cols for plasmid spotting only
gias_plasmid_excerpt_cols = ['Destination Plate Barcode','Destination Well','chain']
chain_letters = ['H','K','L']
echo_spotting_cols = ['Source Plate Barcode', 'Source Well','Destination Plate Barcode','Destination Well', 'Volume']

# =================================
# microbiology
# =================================
cols_trfo = ['Trafo_Barcode', 'Trafo_Well', 'Qtray_Barcode','Qtray_well']
cols_pick = ['Qtray_Barcode','Qtray_well','CulturePlate1_Barcode','CulturePlate1_Well']
cols_mibi = ['GiAS_Barcode','GiAS_Well','Trafo_Barcode', 'Trafo_Well','Qtray_Barcode','Qtray_well','CulturePlate1_Barcode','CulturePlate1_Well']
#
cols_trafo_import = ['specPCR_GiAS_ID', 'Trafo_Barcode', 'Trafo_Well', 'Qtray_Barcode','Qtray_well', 'Colonies']

# =================================
# Antibodies
# =================================
WS_col_sort = ['PlateWell_WorkingStock', 'A_SingleChainList_C::Plasmid Name']
WS_to_drop = ['PlateBarcode_WorkingStock','A_SingleChainList_C::Antibody_ID']
WS_reshaped = ['Transfection_Well','PlasmidName_pDNA1','pDNA1_ID','Well_2','PlasmidName_pDNA2','pDNA2_ID']
trans_cols_reshaped = ['Transfection_ID','PlasmidName_pDNA', 'pDNA_ID']
assign_cols = ['Plasmid_Assignment_ID', 'Transfection_ID', 'PlasmidName_pDNA']
drop_tube_cols = ['Scan Time','Orientation Barcode','Tube Row','Tube Column']
tubes_col_names = ['Aliquot_Barcode', '_2D_Tube_Barcode','Aliquot_well']
htrf_cols_drop  = ['RATIO 665/620*10000', 665, 620, 'HTRF plate']
htrf_after_reshape = ['plate','HTRF1 ug_mL','96well', 'plate2','HTRF2 ug_mL','96well2']
locations = ['LAT', 'Berlin']
transfection_method = 96
harvest_columns = ['Transfection_ID','Aliquot_Barcode', 'Aliquot_well', 'Location','Sent_Date_to_External','_2D_Tube_Barcode','HTRF1 ug_mL','HTRF2 ug_mL','HTRF_Avg ug_mL','Volume_uL','Harvest_Date','Harvest_Day','Transfection_Method']

# ==============
# repicks
# ==============
repick_cols_drop = ['Plating_ID', 'Qtray_Barcode', 'Qtray_well', 'Colonies']
repick_manual = ['BAST_PICK_BARCODE', 'BAST_PICK_WELL', 'CulturePlate1_Barcode', 'CulturePlate1_Well']