# Used to create a frequeny table of this months and last month files.
# The proportions are then compared to make sure that is no large rise or fall in the data

# Creates Frequency Table
def CreateFreqTab(df):
    # Run Frequencies and add group variable
    df_freq = df.apply(pd.value_counts)
    df_freq['Group']= df_freq.index
    
    # Melt/Gather the Frequencies
    df_freqtable = pd.melt(df_freq, id_vars=['Group'], var_name='Variable', value_name='Value')

    # Concatenate Variable and Group into new column. Will be used to merge with other tables
    df_freqtable['LinkVar'] = df_freqtable['Variable'].map(str) + '_' + df_freqtable['Group'].map(str)

    # Remove all frequencies <0
    df_freqtable = df_freqtable.loc[df_freqtable['Value'] >= 0,:]

    # Turn counts into percentages
    df_freqtable['Value'] = df_freqtable['Value']*100/len(df.index)
    
    return df_freqtable


# Compares Frequency Tables
def CompareFreqTab(Old_File, New_File):
    LMF_Freq = CreateFreqTab(Old_File)
    TMF_Freq = CreateFreqTab(New_File)
    
    # Merge Dataframes
    whole = pd.merge(LMF_Freq, TMF_Freq, how='outer', on='LinkVar')

    # Create the percentage difference of each position
    whole['MonthDif']=abs((whole['Value_x']) - (whole['Value_y']))
    
    whole = whole.sort_values('MonthDif', ascending=False)
    # Filter output to differences greater than 5%
    #lmt = 5
    #filt = whole.loc[whole['MonthDif']>=lmt,:]
    # Sort file with largest difference at top
    
    print(whole[['LinkVar', 'Value_x', 'Value_y', 'MonthDif']].head(10))
    print(whole[['LinkVar', 'Value_x', 'Value_y', 'MonthDif']].tail(10))
    
    
# Compare Base File
#file_loc = "r'C:\Users\jpcut\OneDrive\Documents\Anthony\RMR\Mod1_6_attempt"
LMF = pd.read_csv(r'C:\Users\jpcut\OneDrive\Documents\Anthony\RMR\Mod1_6_attempt\Aug21 Mod1-6.csv',index_col="RESPONDENT_ID")
CompareFreqTab(LMF, df_out)
