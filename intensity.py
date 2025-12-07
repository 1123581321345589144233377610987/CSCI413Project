import pandas as pd
data=pd.read_csv("cleaned data/Activity Data Cleaned.csv")
data['intensity']=data['intensity'].fillna('SEDENTARY')
mapping = {'SEDENTARY': 0, 'ACTIVE': 1, 'HIGHLY ACTIVE': 2}
data['intensity']=data['intensity'].map(mapping)
data.to_csv("cleaned data/Activity Data Cleaned.csv")
data.info()