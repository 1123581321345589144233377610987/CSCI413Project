import pandas as pd
import math
import openpyxl
#NOTE: Sleep Data handled separately:
#sleeptime and sleep need to be joined

folderNames = ["Activity Data", "Glucose Data", "Basal Data", "Bolus Data", "Nutrition Data", "Sleep Data", "SleepTime Data"]
folderPrefixes=["Activity", "Glucose", "Basal", "Bolus", "Nutrition", "sleep", "sleeptime"]
fileName=""
path=""
file=""
       
outCount=0
while outCount <len(folderNames):
    path="".join(["data\\",folderNames[outCount],"\\"])
    inCount=0
    subject=2300
    df = pd.DataFrame()
    while inCount < 25:
        subject+=1
        if subject == 2321:
            subject=2401
        if folderNames[outCount]!="SleepTime Data":
            fileName="".join(["UoM",folderPrefixes[outCount], str(subject),".csv"])
        else:
            fileName="".join(["UoM", str(subject),folderPrefixes[outCount],".csv"])
        file="".join([path,fileName])
        print(file)
        try:
            file=pd.read_csv(file)
            file["subjectID"]=subject
            df=pd.concat([df,file],ignore_index=True)
        except FileNotFoundError:
            print("FILE NOT FOUND")
        inCount+=1
    newFile = "".join([folderNames[outCount],".csv"])
    df.to_csv(newFile, index=False)
    outCount+=1
