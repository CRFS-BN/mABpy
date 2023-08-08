
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
dir_output_gias = os.path.join(dir_parent,'07_GiAS_Out') 
dir_import_gias = os.path.join(dir_output_gias, '07_GiAS_imports')
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
dir_knime_baseid = os.path.join(dir_parent,'04_Parse_Out', 'ID_Dictionary', 'ID_Dictionary.xlsx') #get dir dictionary_ID
dir_old_baseid = os.path.join(dir_parent,'04_Parse_Out', 'ID_Dictionary', 'old_files') #get dir dictionary_ID
# =================================
# PATHS PCR3
# =================================
#all xlsx files in intermed files after specPCR
all_partial_imports = os.path.join(dir_partial_imports, '*.xlsx')
#PCR3 primer file
dir_primer_lookup = os.path.join(dir_input,'PCR3_primer.xlsx')
#get all xlsx files in dir_store
all_store_lists = os.path.join(dir_store, '*.xlsx')
# =================================
# PCR3 vars
# =================================
chunk_96 = 96 #96 samples processed oat once

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
# capillary electrophoresis vars
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
# gibson assembly vars
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