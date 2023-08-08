"""
Suport for microbiology workflow

Author: Malwina Kotowicz
E-mail: malwina.kotowicz@dzne.de
"""
import pandas as pd

def insert_colonies(df, col_culture_well, col_colonies):
    """
    Inserts 'Y' to 'Colonies' col if bacterial growth on Qtray fields, 'N' otherwise 
    col_culture_well is col name of culture plate well, col_colonies is a new col name to output the results
    """
    condition_na = pd.isna(df[col_culture_well])
    df.loc[condition_na, col_colonies] = 'N'

    condition_notna = pd.notna(df[col_culture_well])
    df.loc[condition_notna, col_colonies] = 'Y' 
    
    return df

def insert_growth_cultureplate2(df, barcode_no_growth, wells_no_growth):
    """ Adds 'Growth_CulturePlate2' column to df & inserts 'Y' if bacterial growth on CulturePlate2, 'N' otherwise
    barcode_no_growth is culture plt 1 barcode of concerned plt, wells_no_growth is a list of wells with no growth
    
    """
    nogrowth_plates = (df['Colonies'] == 'N')#no growth on qtrays
    df.loc[nogrowth_plates, 'Growth'] = 'N'#when no growth on qtrays, also assign 'N' to growth culture plate2

    for item in wells_no_growth:
        condition = (df['CulturePlate1_Well'] == item.upper()) & (df['CulturePlate1_Barcode'] == barcode_no_growth)
        df.loc[condition, 'Growth'] = 'N'#where well in wells_no_growth list, assign 'N' 

    rest = pd.isna(df['Growth'])#where NaNs (no value yet) in CulturePlate2
    df.loc[rest, 'Growth'] = 'Y' #assign 'Y'
    
    return df

def add_barcodes(df,cul_barcode,glycerol,plasmid, wells):
    """ Add glycerol, plasmid barcodes and wells
    """
    cols = {'GlycerolStock_Barcode':glycerol,'GlycerolStock_Well':wells, 'PLA1_Barcode':plasmid,'PLA1_Well':wells}
    condition = df['CulturePlate1_Barcode'] == cul_barcode # < 1 culture plt in one file
    for key, value in cols.items():
        df.loc[condition,key] = value
    return df

def add_barcodes_repick(df,cul_barcode,glycerol,plasmid, wells):

    """ Add glycerol, plasmid, culture barcodes and wells
    """
    cols = {'CulturePlate1_Barcode':cul_barcode,'CulturePlate1_Well':wells,
            'GlycerolStock_Barcode':glycerol,'GlycerolStock_Well':wells, 'PLA1_Barcode':plasmid,'PLA1_Well':wells}
    
    for key, value in cols.items():
        df[key] = value
        
    return df