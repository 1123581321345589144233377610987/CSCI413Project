import pandas as np
import numpy as pd
files=["Activity", "Glucose", "Nutrition", "Bolus", "Basal", "Sleep"]
ts=["activity_ts","bg_ts", "meal_ts","bolus_ts","basal_ts","sleep_ts"]
prefix="cleaned data/"
suffix="_Data_Aggregated.csv"
#first renaming the timestamp col to be ts for all of them so everything is just a little easier
#also dropping all columns with "unnamed"

i=0
while i < len(files):
    try:
        file=np.read_csv("".join([prefix,files[i],suffix]), index_col=['subjectID',ts[i]])
    except ValueError:
        file=np.read_csv("".join([prefix,files[i],suffix]), index_col=['subjectID','ts'])
    try:
        file['ts']=file[ts[i]]
        file=file.drop(ts[i], axis=1)
    except KeyError:
        print("already done!")
    file = file.loc[:, ~file.columns.str.contains('unnamed', case=False)]
    try: 
        file=file.drop('Unnamed: 0', axis=1)
    except KeyError:
        print("no Unnamed: 0")
    try:
        file=file.drop('')
    except KeyError:
        print("no ''")
    file.to_csv("".join([prefix,files[i],suffix]))
    i+=1


file="".join([prefix,files[0],suffix])
file=np.read_csv(file, index_col=['subjectID','ts'])
i=1

while i<len(files):
    print("".join([prefix,files[i],suffix]))
    print(np.read_csv("".join([prefix,files[i],suffix])).index.name)
    print(np.read_csv("".join([prefix,files[i],suffix])).columns.tolist())
    file=np.merge(file, np.read_csv("".join([prefix,files[i],suffix])), on=['subjectID','ts'], how='outer')
    i+=1
file.to_csv("THE.csv")
