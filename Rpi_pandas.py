# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 15:13:53 2020

@author: fredr
"""
import pandas as pd

#%%
df  = pd.read_csv("Maalinger.csv")
df.columns = ["Date", "Time", "Temp from humidity", "Temp from pressure", "Humidity", "Pressure", "Acceleration"]
df["Date"] = pd.to_datetime(df["Date"],format="%d/%m/%Y").dt.date
df["Time"] = pd.to_datetime(df["Time"],format="%H:%M:%S").dt.time


#%%
# Separerer målingene utifra hvilke dager de ble målt og lagrer en df fra
# hver dag i listen data_from_all_days

def column_values(df, column): # Returnerer alle unike verdier fra en spesifikk kolonne i en dataframe:
    unique_values = list(df[column].sort_values().unique())
    return unique_values


def seperate_by_column_values(df, column): # returnerer en liste med df-er
    dfs = []
    unique_column_vals = column_values(df, column)
    for val in unique_column_vals:
        df_n = df[df[column] == val]
        dfs.append(df_n[:1000])
    return dfs

data_from_all_days = seperate_by_column_values(df, "Date")

#%%
print(df["Acceleration"].mean())
a = str(df["Time"][-1:])