import pandas as pd
from sklearn.preprocessing import StandardScaler
basal=pd.read_csv("combined data//Basal Data.csv")
basal=basal.drop(columns=['Unnamed: 3','Unnamed: 4'])
basal=pd.get_dummies(basal, columns=['insulin_kind'])
short=basal[basal['insulin_kind_R']].copy()
long=basal[basal['insulin_kind_L']].copy()

def outliers(data):
    #dealing with outliers
    #outliers
    #create an empty mask in which to track outliers
    outlier_mask = pd.Series([False] * len(data), index=data.index)
    columns_to_check = data[['basal_dose']]
    #iterate through each column and add outliers to the outlier mask
    for col in columns_to_check:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        #update the outlier_mask - mark it True if there is an outlier in the current col
        outlier_mask = outlier_mask | ((data[col] < lower_bound) | (data[col] > upper_bound))

    #drop all outliers
    return data[~outlier_mask]

short=outliers(short)
long=outliers(long)

scaler=StandardScaler()
long['basal_dose'] =scaler.fit_transform(long[["basal_dose"]])
short['basal_dose'] =scaler.fit_transform(short[["basal_dose"]])

long.to_csv("cleaned data//Long Data Cleaned.csv")
short.to_csv("cleaned data//Short Data Cleaned.csv")