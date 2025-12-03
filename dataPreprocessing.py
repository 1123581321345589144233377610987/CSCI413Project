# Elanor Fugate and Sedona Szczepaniak
# CSCI413 - Advanced Data Science
# Type 1 Diabetes Glucose Prediction Final Project

# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


# read in big aggregated csv and preliminary column drop
big_df = pd.read_csv("THE.csv")

big_df.drop(columns=["Unnamed: 0.1", "Unnamed: 0", "insulin_kind_L", "insulin_kind_R"], inplace=True)

# iterate over each subject of interest
subject_ids = [2301, 2304, 2307, 2308, 2309]

for subject_id in subject_ids:

    df = big_df[ big_df["subjectID"] == subject_id ].copy()
    df.reset_index(drop=True, inplace=True)

    # ---------- FEATURE ENGINEERING AND NULL HANDLING ----------
    # fill nutrition nulls
    nutrition_cols = ["carbs_g", "prot_g", "fat_g"]
    for col in nutrition_cols:
        df[col].fillna(0, inplace=True)

    # add time of day column
    times_of_day = [""] * len(df["ts"])
    for i, timestamp in enumerate(df["ts"]):
        time = timestamp.split()[1]
        hour = int(time[:2])
        time_of_day = ""

        if (hour < 5) or (hour >= 22):
            times_of_day[i] = "Night"
        elif hour < 12:
            times_of_day[i] = "Morning"
        elif hour < 18:
            times_of_day[i] = "Afternoon"
        else:
            times_of_day[i] = "Evening"

    df["time_of_day"] = times_of_day

    # add sleep status column
    sleep_statuses = [False] * len(df["sleep_level"])
    sleep_null_map = df["sleep_level"].isnull()

    for i, sleep_level in enumerate(df["sleep_level"]):
        is_sleeping = False
        if ( sleep_null_map[i] and df["time_of_day"][i] == "Night" ) or ( sleep_level == 1 ):
            is_sleeping = True        
        sleep_statuses[i] = is_sleeping

    df["is_asleep"] = sleep_statuses

    # handle activity nulls once that's a thing
    # handle basal and bolus nulls

    # remove glucose nulls if asleep
    df = df[ ~(df["value"].isnull() & df["is_asleep"]) ]

    # remove rows with no relevant features
    df = df[ ~( (df["carbs_g"] == 0) & df["bolus_dose"].isnull() & df["basal_dose"].isnull()
               & df["active_Kcal"].isnull() & df["heart_rate"].isnull() ) ]

    # get indices for glucose nulls
    null_glucose_inds = []
    glucose_null_map = df["value"].isnull()

    for i, isNull in enumerate(glucose_null_map):
        if isNull:
            null_glucose_inds.append(i)

    # drop if more than 6 consecutive hours of null glucose values
    to_drop = []

    for i, ind in enumerate(null_glucose_inds):
        if (null_glucose_inds[i:i+6] == list(range(ind, ind+6))) or (null_glucose_inds[i-5:i+1] == list(range(ind-5, ind+1))):
            to_drop.append(ind)

    df.drop(df.index[to_drop], inplace=True)

    # reset indices for glucose nulls
    null_glucose_inds = []
    glucose_null_map = df["value"].isnull()

    for i, isNull in enumerate(glucose_null_map):
        if isNull:
            null_glucose_inds.append(i)

    # fill remaining glucose nulls with most recent valid value
    for i in null_glucose_inds:
        replacement_ind = i
        while replacement_ind in null_glucose_inds:
            replacement_ind -= 1
        df.iloc[i, df.columns.get_loc("value")] = df.iloc[replacement_ind, df.columns.get_loc("value")]

    # convert glucose values from mmol/L to mg/dL because we're not British
    # (this isn't actually important but just for my sake)
    df["value"] *= 18

    # drop all the columns we don't need anymore
    cols_to_drop = ["subjectID", "ts", "active_Kcal", "step_count", "distance_m", "active_time_s",
                    "motion_intensity_mean", "met", "motion_intensity_max", "heart_rate",
                    "current_activity_type_intensity", "stress_level_value", "resting_heart_rate", "sleep_level"]
    df.drop(columns=cols_to_drop, inplace=True)

    # ---------- FEATURE SCALING AND ENCODING ----------
    # establish which columns are numeric vs categorical
    numeric_cols = ["value", "carbs_g", "prot_g", "fat_g"]  # , "bolus_dose", "basal_dose"]
    categorical_cols = ["time_of_day"]  # , "activity_intensity"]
    # leaving is_asleep because it's already a Boolean

    # normalize numeric columns
    df_transformed = df.copy()
    scaler = StandardScaler()
    df_transformed[numeric_cols] = scaler.fit_transform(df_transformed[numeric_cols])

    # one-hot encode categorical columns
    df_transformed = pd.get_dummies(df_transformed, columns=categorical_cols)

    # ---------- SAVE UPDATED DATA ----------
    # save cleaned/engineered data to csv (very last step)
    df_transformed.to_csv(f"scaledData/{subject_id}.csv", index=False)
    print(f"Saving {subject_id}.csv...")
