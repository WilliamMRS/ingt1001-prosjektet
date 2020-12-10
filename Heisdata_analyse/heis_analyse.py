3#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 11:32:31 2020

@author: erlingkornstadsmenes
"""

import pandas as pd
import numpy as np
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
#%%
def findLowestValues(window, day, df):
    lowestValues = []
    i = 0 # Index to count inside window
    lowestPressure = 10000 # random tall som e høyere enn alle målinger
    for value in df[day].Pressure:
        if(i >= window):
            lowestValues.append(lowestPressure)
            lowestPressure = 10000 # reset lowestPres
            i = 0 # reset i
        if(lowestPressure > value):
            lowestPressure = value
        i += 1
    return lowestValues

def findHighestValues(window, day, df):
    highestValues = []
    i = 0 # Index to count inside window
    highestPressure = 0 # random tall som e høyere enn alle målinger
    for value in df[day].Pressure:
        if(i >= window):
            highestValues.append(highestPressure)
            highestPressure = 0 # reset lowestPres
            i = 0 # reset i
        if(highestPressure < value):
            highestPressure = value
        i += 1
    return highestValues
#%%
    
def PlotDay(day_index, df):
    start = 0
    stop = len(df[day_index]["Pressure"])
    print(len(df[day_index]["Pressure"]))
    # Data to plot
    
    fig, ax=plt.subplots(figsize=(12,8))
    plt.title("26. Novemeber")
    df[day_index].plot(x="Time", y=["Pressure"], ax=ax, color="yellow")
    ax.set_ylabel = "Pressure"
    ax.set_xlim(start,stop)
    #maxY = data_from_all_days[day_index]["Pressure"][start:stop].max()
    #minY = data_from_all_days[day_index]["Pressure"][start:stop].min()
    ax.set_ylim(1007,1018) # use integers to offset, making graph readable
    
    # Building accel graph
    # =============================================================================
    # ax2=ax.twinx() # Cloning previous ax
    # data_from_all_days[0].plot(x="Time", y=["Acceleration"], ax=ax2, color="green")
    # ax2.set_xlim(start,stop)
    # 
    # maxY2 = data_from_all_days[0]["Acceleration"][start:stop].max()
    # minY2 = data_from_all_days[0]["Acceleration"][start:stop].min()
    # print(maxY2)
    # ax2.set_ylim(minY2 - 1,maxY2 + 2) # use integers to offset, making graph readable
    # =============================================================================
    
    #ts = pd.Series(df['Pressure'].values) #omitting index=df['Time'] cause it's not helpful in this instance
    
    lv = findLowestValues(1800, day_index, df)
    lvSeries = pd.Series(lv)
    print(lvSeries.head(10))
    
    ax3=ax.twiny()
    lvSeries.plot.line()
    ax3.set_xlabel = "Timestep (s)"
    ax3.set_ylabel = "Pressure"
    ax3.set_xlim(0,lvSeries.size)
    #maxY = lvSeries.max()
    #minY = lvSeries.min()
    #ax3.set_ylim(1008,1024) # use integers to offset, making graph readable
    
    
    hv = findHighestValues(1800, day_index, df)
    hvSeries = pd.Series(hv)
    print(hvSeries.head(10))
    
    ax4 = ax3.twiny()
    hvSeries.plot.line(color="red")
    ax4.set_xlim(0,lvSeries.size)
    #maxY = hvSeries.max()
    #minY = hvSeries.min()
    #ax4.set_ylim(1008,1024) # use integers to offset, making graph readable
    plt.show()
    return [hvSeries, lvSeries]

#%%

# Straighten graph, then cut lines to decide where the stories go.
# Reference point for straighten is at theend of the graph
# Cut away the last few datapoints before plotting day [7] 26. November

# finn stigningstallet til punktene fra min og max grafene og forskyv rådatapunktene basert på verdien til
# min/max grafene i forhold til referansepunktet som er å slutten.
novemberData = []
novemberData.append(data_from_all_days[7].iloc[0:20300]) #Grab data that's useful
novemberData.append(data_from_all_days[7].iloc[0:20300]) #Grab data that's useful again for later
#PlotDay(7, data_from_all_days)
minmaxseries = PlotDay(0, novemberData)

print(minmaxseries[0])

# use end of graph as reference
referencePressureRange = minmaxseries[0][10] + minmaxseries[1][10]
print(referencePressureRange)

offsetvals = []
for i in range(0,11):
    offsetvals.append(referencePressureRange - (minmaxseries[0][i] + minmaxseries[1][i]))
    
print(offsetvals)

# push all data up by the offsetvals (this is a crude method, but works for early approximation)
window = 1800 # Important that this is the same as the windows used for making mimmaxseries.
i = 14
y = 0

print(novemberData[1]["Pressure"][i])
print(offsetvals[y])
print(len(novemberData))
print("November data over")

for value in novemberData[0]["Pressure"]:
    for value in novemberData[0].Pressure:
        if(y >= 11):
            break
        if (i < window):
            novemberData[1]["Pressure"][i + y*1800] = value + offsetvals[y]/2
            i += 1
        else:
            i = 0 # reset i
            y += 1 # next window offset

PlotDay(1, novemberData)












