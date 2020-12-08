#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 11:32:31 2020

@author: erlingkornstadsmenes
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import calendar

#Importere dataset

df = pd.read_csv("/Users/erlingkornstadsmenes/Documents/GitHub/ingt1001-prosjektet/Datasets/Maalinger.csv")
df.columns = ["Date", "Time", "Temp_hum", "Temp_pres", "Humidity", "Pressure", "Acceleration"]
df["Date"] = pd.to_datetime(df["Date"])


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


#?

a = str(df["Time"][-1:])


#Sortere etter ukedag(test1)(Kan fjernes)

plt.style.use("fivethirtyeight")

dates = pd.date_range(start=pd.datetime(2020,11,25), end=pd.datetime(2020,12,7),
                      periods=None, freq='D', tz=None, normalize=False, name=None, closed=None)
                      
values = [100*random.random() for i in range(len(dates))]
values[:10]

ukedag_df = pd.DataFrame(index=dates, data=values)
ukedag_df.reset_index(inplace=True)
ukedag_df.columns = ['Date', '?']
ukedag_df.head()

ukedag_df['day_of_week'] = ukedag_df['Date'].apply(lambda x: x.weekday())
ukedag_df['day_of_week'] = ukedag_df['day_of_week'].apply(lambda x: calendar.day_name[x])
ukedag_df.head()


#Sortere etter ukedag(test2)(Kan fjernes)

df['Weekday'] = df['Date'].dt.dayofweek


#Regne ut gjennomsnitt for renere plotting?(hvor ofte bør gjennomsnittet regnes?)(test2)


#Plotte datasettene

data_from_all_days[0].plot(x="Time", y=["Humidity", "Pressure", "Acceleration"])
plt.show()

data_from_all_days[0].plot(x="Time", y=["Pressure"])
plt.show()

data_from_all_days[0].plot(x="Time", y=["Humidity", "Acceleration"])
plt.show()
