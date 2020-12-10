3#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 11:32:31 2020

@author: erlingkornstadsmenes
"""

import pandas as pd
import matplotlib.pyplot as plt

#Importere dataset
df = pd.read_csv("./Maalinger.csv")
df.columns = ["Date", "Time", "Temp_hum", "Temp_pres", "Humidity", "Pressure", "Acceleration"]
print(df.describe())
print(df.head(5))
df.drop_duplicates() #Fjerne duplikatverdier

# Separerer målingene utifra hvilke dager de ble målt og lagrer en df fra
# hver dag i listen data_from_all_days

def column_values(df, column): # Returnerer alle unike verdier fra en spesifikk kolonne i en dataframe:
    unique_values = list(df[column].sort_values().unique())
    return unique_values

def separate_by_column_values(df, column): # returnerer en liste med df-er
    dfs = []
    unique_column_values = column_values(df, column)
    for val in unique_column_values:
        df_n = df[df[column] == val]
        dfs.append(df_n)
    return dfs

data_from_all_days = separate_by_column_values(df, "Date")
#print(data_from_all_days)

a = str(df["Time"][-1:])

#Plotte dataen på en hensiktsmessig måte
#Hvilken etasje står heisen mest i?

# =============================================================================
# ax = plt.subplot(111)
# data_from_all_days[0].plot(x="Time", y=["Pressure"], ax=ax)
# ax.set_xlim(8000,8400)
# plt.show()
# 
# ax = plt.subplot(111)
# data_from_all_days[0].plot(x="Time", y=["Acceleration"], ax=ax)
# ax.set_xlim(8000,8400)
# plt.show()
# 
# ax = plt.subplot(111)
# data_from_all_days[0].plot(x="Time", y=["Humidity"], ax=ax)
# ax.set_xlim(8000,8400)
# plt.show()
# =============================================================================

start = 1000
stop = 1500
# Data to plot

fig, ax=plt.subplots()
data_from_all_days[0].plot(x="Time", y=["Pressure"], ax=ax, color="blue")
ax.set_xlabel = "Timestep (s)"
ax.set_ylabel = "Pressure"
ax.set_xlim(start,stop)
maxY = data_from_all_days[0]["Pressure"][start:stop].max()
minY = data_from_all_days[0]["Pressure"][start:stop].min()
ax.set_ylim(minY - 1,maxY + 3) # use integers to offset, making graph readable

# Building accel graph
ax2=ax.twinx() # Cloning previous ax
data_from_all_days[0].plot(x="Time", y=["Acceleration"], ax=ax2, color="green")
ax2.set_xlim(start,stop)

maxY2 = data_from_all_days[0]["Acceleration"][start:stop].max()
minY2 = data_from_all_days[0]["Acceleration"][start:stop].min()
ax2.set_ylim(minY2 - 7,maxY2 + 2) # use integers to offset, making graph readable

plt.show()

ts = pd.Series(df['Pressure'].values) #omitting index=df['Time'] cause it's not helpful in this instance
print(ts)