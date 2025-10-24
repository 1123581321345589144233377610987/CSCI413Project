

"""
#fix long
long = pd.read_csv("".join([path,"Long_Data_Aggregated.csv"]))
# reset index so basal_ts becomes a column
long = long.reset_index()

# compute daily totals
long['basal_ts'] = pd.to_datetime(long['basal_ts'])
dailysum = (
    long.groupby(['subjectID', long['basal_ts'].dt.date])['basal_dose']
    .sum()
    .reset_index()
    .rename(columns={'basal_dose': 'daily'})
)

# merge back to long data
long['daily']=dailysum['daily']
#long = pd.merge(long, dailysum, on=['subjectID', 'date'], how='left')
# reset index so basal_ts becomes a column
long = long.reset_index()

# overwrite basal_dose with daily value
long['basal_dose'] = long['daily']/24
long.drop(columns=['daily'], inplace=True)
long['insulin_kind_L']=True
long['insulin_kind_R']=False

# save updated file
long.to_csv("".join([path, "Long_Data_Aggregated.csv"]), index=False)

short=pd.read_csv("".join([path,"Short_Data_Aggregated.csv"]))
short['insulin_kind_R']=True
short['insulin_kind_L']=False
basal=pd.concat([short, long], ignore_index=True)
basal = basal.reset_index(drop=True) 
basal.to_csv("".join([path, "Basal_Data_Aggregated.csv"]), index=False)

"""
long=pd.read_csv("".join([path,"Long_Data_Aggregated.csv"]))
long = long.set_index(['subjectID', 'basal_ts'])
dailysum=long.groupby(['subjectID',long['basal_ts'].dt.date])['basal_dose'].sum().reset_index().rename(columns={'basal_dose': 'daily'})
dailysum['hourly']=dailysum['daily']/24
long = pd.merge(long, dailysum[['subjectID', 'date', 'hourly_dose']], on=['subjectID', 'date'],how='left')
long['basal_dose'] = long['hourly']
long.drop(columns=['hourly', 'date'], inplace=True)

long.to_csv("".join([path, "Long_Data_Aggregated.csv"]))
short=pd.read_csv("".join([path,"Short_Data_Aggregated.csv"]))
basal=pd.concat([short, long])
basal.to_csv("".join([path, "Basal_Data_Aggregated.csv"]))
"""