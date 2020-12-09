#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 11:32:31 2020

@author: erlingkornstadsmenes
"""

import pandas as pd
import matplotlib.pyplot as plt

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


#Plotte datasettene(Plotte hver 100th eller 1000th måling?)
#Hvilken etasje står heisen mest i?(Må skrive en funksjon for å forholdet mellom etasjene?)

data_from_all_days[0].plot(x="Time", y=["Humidity", "Pressure", "Acceleration"])
plt.show()

data_from_all_days[0].plot(x="Time", y=["Pressure"])
plt.show()

data_from_all_days[0].plot(x="Time", y=["Humidity", "Acceleration"])
plt.show()

df.plot(x="Date", y=["Humidity", "Acceleration"])
plt.show()

df.plot(x="Date", y=["Pressure"])
plt.show()

df.plot(x="Date", y=["Humidity", "Pressure", "Acceleration"])
plt.show()
