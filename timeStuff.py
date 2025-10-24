import pandas as pd

path="cleaned data/"
suffix=" Data Cleaned.csv"

def process(file,target,function):
    def sum(group):
        g = group[target].resample('h').sum()
        g = g.asfreq('h')
        g = g.to_frame(name=target)
        return g
    def avg(group):
        g = group[target].resample('h').mean()
        g = g.asfreq('h')
        g = g.to_frame(name=target)
        return g

    data="".join([path,file,suffix])
    data=pd.read_csv(data)
    try:
        ts="".join([file.lower(),'_ts'])
        data[ts]=pd.to_datetime(data[ts], dayfirst=True, format='mixed')
    except KeyError:
        ts=input(f"Please enter name of timestamp col for {file}: ")
        if(len(ts)<3 or ts[-3:]!='_ts'):
            ts="".join([ts,'_ts'])
        data[ts]=pd.to_datetime(data[ts], dayfirst=True)
   
    data=data.set_index(ts)
    match function:
        case 'sum':
            data=data.groupby('subjectID').apply(sum)
        case 'avg':
            data=data.groupby('subjectID').apply(avg)
        
    #data.fillna(0, inplace=True)
    print(data.head())
    print(data.info())

    newfile="".join([path,file,"_Data_Aggregated.csv"])
    data.reset_index(inplace=True)
    data.to_csv(newfile, index=False)

#process

process('Bolus','bolus_dose','sum')
process('Glucose','value','avg')
process('Long', 'basal_dose', 'sum')
process('Short', 'basal_dose', 'sum')


#meal_type,carbs_g,prot_g,fat_g

#process('Nutrition','carbs_g','sum')