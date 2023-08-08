"""
Functions for plt manipulations

Author: Malwina Kotowicz
E-mail: malwina.kotowicz@dzne.de
"""
import numpy as np
import pandas as pd

def split_specPCR(df, number_of_samples):
    
    """Gets floor and modulo of df split by number_of_samples
    
    Input:
    
    number_of_samples (int)

    Returns floor, modulo
    """
    floor, modulo = divmod(len(df),number_of_samples)
    
    return floor, modulo

def get_specPCR_list(all_samples, store_list):
    
    """ Gets an excerpt of all samples (df) - new store list (df)

    """
    #take first N samples: from the beginning of current_store_list up to start of final store list
    specPCR_list = all_samples.iloc[:(len(all_samples) - len(store_list))]
    
    return specPCR_list

def get_plt_numbers(last_plt_number, number_of_plts):
    
    """Finds plate numbers for specPCR (cele, gias) plates. Converts to five digit integer format
    
    Input: 
    last_plt_number -- int
    
    Returns:
    
    plate_numbers -- list of converted values
    
    """
    plate_numbers = []
    for i in range(number_of_plts):
        last_plt_number = last_plt_number + 1
        number = '{0:0=5d}'.format(int(last_plt_number))
        plate_numbers.append(number)
        
    return plate_numbers

def get_pcr3(last_plt_num, num_plts):
    """
    Gets specPCR copy plt numbers, assuming 2 specPCRs going to 1 ldv plt.
    
    last plt number is last specPCR copy number, num_plts is the number of specPCR plates (not copy!)
    to use
    
    """
    plt_numbers = []
    floor, mod = divmod(num_plts,2) #get modulo of number of plts by 2
    
    for i in range(floor): #each ldv plt is used twice
        last_plt_num = last_plt_num + 1 #add 1 to last plt num
        number = '{0:0=5d}'.format(int(last_plt_num)) #convert
        plt_numbers.extend([number] * 2) #append twice
        

    if mod != 0: # e.g., 3 specPCR plt, need to use 2x ldv plt
        last_plt_num = last_plt_num + 1 #last plt num is incremented above
        number = '{0:0=5d}'.format(int(last_plt_num))
        plt_numbers.append(number)
            
    return plt_numbers


def get_wells(num_plts, raster1, raster2): 
    
    """ Gets the wells for specPCR copy plt, assuming 2 specPCRs going to 1 ldv plt (raster to be specified,
    usually A1_A3 and A2_A4)
    
    num_plts is the number of specPCR plates (not copy!), raster1, raster2 are prefered rasters on ldv 
    (1st specPCR plt gets copied to raster 1, 2nd PCR plt to raster2)
    """
    rasters = []
    
    for i in range(num_plts): #plts to specPCR
        if (i % 2) == 0: 
            raster = raster1.values  #this is first plt, index 0 --> 0/2=0
        else:
            raster = raster2.values #this is second plt, index 1 --> 1/2=0.5
            
        rasters.append(raster)
        
    return rasters

def split_into_chunks(df,num_of_chunks, chunk):
    
    """Splits df into equal chunks by num_of_chunks, creates pd df out of chunk of interest (chunk)
    
    """
    specPCR_list_split = pd.DataFrame(np.array_split(df,num_of_chunks)[chunk])
    
    return specPCR_list_split
    
def reorder_cols(df, df_to_reorder_by):
    
    """ 
    
    Reorders cols in df based on df_to_reorder_by, saves the original index from df_to_reorder_by as 'Index' col
    
    Parameters:
    
    df -- dataframe to be modified
    df_to_reorder_by -- dataframe to use as a template for columns' order
    
    Returns:
    df -- modified dataframe
    
    """
    
    
    df = df.reindex(df_to_reorder_by.columns, axis=1) #reorder cols in df_new based on df_store col order 
    df['Index'] = df.index #save original index from df_to_reorder_by as 'Index' col in df
    
    return df

def drop_rename(df, cols_drop, cols_new_names):
    """Drops cols and renames remaining ones
    """
        
    df.drop(columns=cols_drop,inplace=True)
    df.columns = cols_new_names
        
    return df

def reshape_to_long(df,col_after_reshape):
    """Transpose to longer by moving vals to row below. Cuts df in half. Mst be ordered col-wise
    col_after_reshape is new column names
    """
    df = pd.DataFrame(np.reshape(df.values,(-1,int(len(df.columns)/2))), columns=col_after_reshape)
    return df

def reshape_to_wide(df, col_after_reshape):
    """Transpose to wider by moving vals to new cols. 
    col_after_reshape is new column names
    """
    df = pd.DataFrame(np.reshape(df.values,(-1,int(len(df.columns)*2))), columns=col_after_reshape)
    return df

def repeat_raster(raster_col, df_to_fillup):
    """Gets the well values based on raster parsed and repeats it n-times to match the lenght of df
    raster_col is the raster to use, df_to_fillup is the reference df, used to get n-times 
    """
    wells = pd.concat([raster_col]*int(len(df_to_fillup)/96), ignore_index=True)
    return wells

def insert_col_at_end(df,col_name,col_val):
    """Inserts col with col_name and col_val at the end of df
    """
    df.insert(len(df.columns)-1, col_name, col_val)

    return df