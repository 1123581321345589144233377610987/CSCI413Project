import pandas as pd
path="cleaned data//"
long = pd.read_csv("".join([path,"Long_Data_Aggregated.csv"]))
short=pd.read_csv("".join([path,"Short_Data_Aggregated.csv"]))

long["basal_ts"]=pd.to_datetime(long["basal_ts"])

"""
for i in long.groupby(['subjectID', long['basal_ts'].dt.date]):
    i['basal_dose']=max(i['basal_dose'])/24
"""

long['basal_dose'] = (
    long.groupby(['subjectID', long['basal_ts'].dt.date])['basal_dose']
    .transform('sum') / 24
)

long.to_csv("".join([path,"Long_Data_Aggregated.csv"]))

basal=pd.concat([short, long])
basal.to_csv("".join([path,"Basal_Data_Aggregated.csv"]), index=False)