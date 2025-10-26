import pandas as pd

path="cleaned data/"
suffix=" Data Cleaned.csv"

def process(file,target,function, mode):
    def sum(group):
        g = group[target].resample('h').sum()
        g = g.asfreq('h')
        try:
            g = g.to_frame(name=target)
            return g
        except AttributeError:
            return g
    def avg(group):
        g = group[target].resample('h').mean()
        g = g.asfreq('h')
        try:
            g = g.to_frame(name=target)
            return g
        except AttributeError:
            return g
    def max(group):
        g = group[target].resample('h').max()
        g = g.asfreq('h')
        try:
            g = g.to_frame(name=target)
            return g
        except AttributeError:
            return g
    def min(group):
        g = group[target].resample('h').min()
        g = g.asfreq('h')
        try:
            g = g.to_frame(name=target)
            return g
        except AttributeError:
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
        data[ts]=pd.to_datetime(data[ts], dayfirst=True, format='mixed')
   
    data=data.set_index(ts)
    match function:
        case 'sum':
            data=data.groupby('subjectID').apply(sum)
        case 'avg':
            data=data.groupby('subjectID').apply(avg)
        case 'max':
            data=data.groupby('subjectID').apply(max)
        case 'min':
            data=data.groupby('subjectID').apply(min)
        
    data.fillna(0, inplace=True)
    print(data.head())
    print(data.info())
    if mode==1:
        newfile="".join([path,file,"_Data_Aggregated.csv"])
        data.reset_index(inplace=True)
        data.to_csv(newfile, index=False)
    else:
        return data

#process
"""
process('Bolus','bolus_dose','sum', 1)
process('Glucose','value','avg', 1)
process('Long', 'basal_dose', 'sum', 1)
process('Short', 'basal_dose', 'sum', 1)
process('Nutrition',['carbs_g','prot_g','fat_g'],'sum', 1)
"""


####ACTIVITY#####
#not sure what to do with
#start_time_s - take min?, but what if they didn't exercize the whole hour? Maybe just drop?
#start_time_offset_s - offset from WHAT??
#met - what is this???

#duration_s - need to look into, could be max or sum or maybe even average depending
#on the specifics of what it actually means

#index
#activity_ts,subjectID

#categorical ffill
#activity_type, intensity?

#sum
#active_Kcal,step_count,distance_m,active_time_s

#average
#intensity, motion_intensity_mean
#NO INTENSITY - that is categorical and a string

#max
#motion_intensity_max

ActSum=process('Activity', ['active_Kcal','step_count','distance_m','active_time_s'], 'sum',0)
ActAvg=process('Activity', ['motion_intensity_mean'], 'avg',0)
ActMax=process('Activity', ['motion_intensity_max'], 'avg',0)
merged = pd.merge(ActSum, ActAvg, on=['subjectID', 'activity_ts'], how='outer')
merged = pd.merge(merged, ActMax, on=['subjectID', 'activity_ts'], how='outer')
merged.to_csv("".join([path,"Activity_Data_Aggregated.csv"]))
merged.head()
merged.info()

###SLEEEEEP#######

#sleep_level - need to look into to see how it works
#possibly average or ffill if it's more like sleep stages?

#index
#sleep_ts,subjectID

#sum

#average
#heart_rate,current_activity_type_intensity,stress_level_value,resting_heart_rate

#categorical ffill
#

#idea: could create new cols like max and min heart rate (would still be over the 5 minute period though)