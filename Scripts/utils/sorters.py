
"""
Functions for plate sorting and alike

Author: Malwina Kotowicz
E-mail: malwina.kotowicz@dzne.de
"""
import pandas as pd

def sort_categorically(df, sorter, column_to_category, columns_to_sort_by):
    """Sorts dataframe (df) categorically by setting chosen column's values to category type (column_to_category), setting hierarchy of these categries (sorter) and then sorting by values in colums specified (columns_to_sort_by)
    
    Parameters:
    
    df -- dataframe to be modified
    column_to_category (str) -- column to set as category type
    sorter (list) -- list of values to set hierarchy to categories 
    columns_to_sort_by (list, str) -- column or list of columns to sort by 
    
    Returns:
    
    df -- modified dataframe 
    """

    #sort samples by raster (as in sorter) 
    df[column_to_category] = df[column_to_category].astype("category") #change type to cat
    df[column_to_category].cat.set_categories(sorter, inplace=True)#set the sorter as categories hierarchy
    df.sort_values(by=columns_to_sort_by, inplace=True)#sort first by cDNA (useful when more than one cDNA plates analysed at once), then sorter raster
    
    return df

def unique_non_null(df):
    """Gets unique vals while ignoring nan"""
    return df.dropna().unique()