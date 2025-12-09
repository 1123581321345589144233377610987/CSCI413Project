import pandas as np
import datetime as dt
file=np.read_csv("THE.csv")
print(file['value'].describe())
file=
"""
print(file.info())
print(file.isna().sum())
print(file.isna().sum()/len(file))

file['ts']=np.to_datetime(file["ts"])
file = file[file["ts"] <= dt.datetime(2026,1,1)]
print(file.info())
print(file.isna().sum())
print(file.isna().sum()/len(file))
file.to_csv('THE.csv')
"""