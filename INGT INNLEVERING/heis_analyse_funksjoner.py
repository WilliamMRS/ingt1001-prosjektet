#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None  # default='warn'
#Importere dataset
df = pd.read_csv("./Maalinger.csv")
df.columns = ["Date", "Time", "Temp_hum", "Temp_pres", "Humidity", "Pressure", "Acceleration"]
df.drop_duplicates() #Fjerne duplikatverdier

vmin1 = 900
vmax1 = 1050
column1 = "Pressure"

vmin2 = 5
vmax2 = 16
column2 = "Acceleration"

df = df[df[column1].between(vmin1, vmax1)]
df = df[df[column2].between(vmin2, vmax2)]

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
    
# PLots a day from a dataframe.
# needs a dataframe array, the day of the df-array, column. upper and lower shows minmax lines. hline will plot floors.
def PlotDay(df, day_index, column, plotUpperAndLower, hline, name):
    start = 0
    stop = len(df[day_index][column])

    fig, ax=plt.subplots(figsize=(14,8))
    plt.title(name)
    df[day_index].plot(x="Time", y=[column], ax=ax, color="green")
    ax.set_ylabel = column
    ax.set_xlim(start,stop)
    ax.set_ylim(df[day_index][column].max()+1, df[day_index][column].min()-1)
    
    if(hline):
        for line in hline:
            ax.axhline(y=line)  

    if(plotUpperAndLower):
        lv = findLowestValues(1800, day_index, df)
        lvSeries = pd.Series(lv)
        ax3=ax.twiny()
        lvSeries.plot.line()
        ax3.set_xlabel = "Timestep (s)"
        ax3.set_ylabel = column
        ax3.set_xlim(0,lvSeries.size)        
        hv = findHighestValues(1800, day_index, df)
        hvSeries = pd.Series(hv)
        ax4 = ax3.twiny()
        hvSeries.plot.line(color="red")
        ax4.set_xlim(0,lvSeries.size)
    plt.show()
    if(plotUpperAndLower):
        return [hvSeries, lvSeries]
        
floorLevels = [1016.3,1015.75,1015.25,1014.95,1014.55,1013.95,1013.5,1013.2,1012.8] 
# 9 etasjer, bestemt ved hjelp av å trekke lineære vannrette linjer over punkt hvor dataene platået

def createAdjustedGraphs(df, dataRange, nameOfGraph):
    # finn stigningstallet til punktene fra min og max grafene og forskyv rådatapunktene basert på verdien til
    # min/max grafene i forhold til referansepunktet som er å slutten.
    novemberData = []
    df = df.reset_index()
    novemberData.append(df), novemberData.append(df), novemberData.append(df) # Dataframes som blir brukt nedenunder
    # ----------------------------- Plot raw data with minmax
    minmaxseries = PlotDay(novemberData, 0, "Pressure", True, False, nameOfGraph)
    # Finner summen av topp og bunn snitt verdier. Ser på forskjellen mellom de 10 blokkene og den alle siste som brukes som referansepunkt
    referencePressureRange = minmaxseries[0][len(minmaxseries[0])-1] + minmaxseries[1][len(minmaxseries[1])-1]
    offsetvals = []
    for i in range(0,len(minmaxseries[0])):
        offsetvals.append(referencePressureRange - (minmaxseries[0][i] + minmaxseries[1][i]))
    # ----------------------------- Dytt all dataen opp med offsets (Ikke perfekt men er en god start)
    window = 1800 # Important that this is the same as the windows used for making mimmaxseries.
    i = 0
    y = 0
    for value in novemberData[1].Pressure:
        if(y >= len(minmaxseries[0])):
            break
        if (i < window):
            novemberData[1]["Pressure"][i + y*window] = value + offsetvals[y]/2
            i += 1
        else:
            i = 0 # reset i
            y += 1 # next window offset
    #PlotDay(novemberData, 1, "Pressure", True, False, nameOfGraph)
    # ----------------------------- Om 0 er forskjøvet med 8 millibar og 1 er forskjøvet med 7 millibar er formelen:
    # newDatapoint = oldDatapoint + (8-7)/1800 * (1800-i), hvor i er det datapunktet som blir forskjøvet i denne rammen.
    i = 0
    y = 0
    for value in novemberData[2].Pressure:
        if(y >= len(minmaxseries[0])-1): # end one earlier, this may skew data little bit. But it shouldn't as it's rather close to reference at this point.
            break
        if (i < window):
            newValue = value + (offsetvals[y]-offsetvals[y+1])/2 /window * (window-i)
            novemberData[2]["Pressure"][i + y*window] = newValue
            i += 1
        else:
            i = 0 # reset i
            y += 1 # next window offset  
    #PlotDay(novemberData, 2, "Pressure", True, False, nameOfGraph)
    cutNovemberData = []
    cutNovemberData.append(novemberData[2].iloc[0:dataRange])
    PlotDay(cutNovemberData, 0, "Pressure", True, floorLevels, nameOfGraph)
    return cutNovemberData

# We've compensated for the weather changing the ambient pressure by finding the min-max range and
# aligning the datapoints to a fixed reference point, in this case the last 1800 datapoints.
# This way, the pressure data represents each floor with more or less the same values, making it
# possible to read what floor the elevator is on at a given time, if we represent the floors as given
# value-steps/ranges. We know there are 9 floors in total and we assume the elevator has visited them
# all in a given day.

def modifyPressureGraph(): # Kind of digitizes the previous graph
    # Decide set limits and modify the pressure graph
    newDataPoints = []
    for value in (cutNovemberData[0]["Pressure"]):
        foundLimits = False
        upperval = 0 # higher level selected for comparison
        lowerval = 0 # lower value selected for comparison
        
        for i in range(0, len(floorLevels)): #loop through all floorlevels
            if(value > floorLevels[i]):
                foundLimits = True
                if(i != 0):
                    upperval = floorLevels[i-1] # If value is greater than this floorlevel, the last floorlevel was uppervalue.
                    lowerval = floorLevels[i] # if value is greater than this, this means that this is the lower level.
            if(i == len(floorLevels)-1 and foundLimits == False):
                #print("LOW:", floorLevels[i])
                newDataPoints.append(floorLevels[i])
                break
            # figure out what value is closest to the value looking for.
            if(foundLimits):
                upperdiff = abs(upperval - value)
                lowerdiff = abs(lowerval - value)
                if upperdiff > lowerdiff: # lowerdiff is closest, pick lowerval
                    newDataPoints.append(lowerval)
                    break
                else:
                    newDataPoints.append(upperval)
                    break
    
    # Build dataframe with new values
    digitizedNovemberData = []
    digitizedNovemberData.append(pd.DataFrame())
    digitizedNovemberData[0].insert(0, "Pressure", pd.Series(newDataPoints), True)
    resetDf = cutNovemberData[0].reset_index(drop=True)
    digitizedNovemberData[0].insert(1, "Time", resetDf["Time"], True)
    return digitizedNovemberData
    
    
data_from_all_days = separate_by_column_values(df, "Date")

cutNovemberData = createAdjustedGraphs(data_from_all_days[0].iloc[0:20300], 20300, "1. Desember")
cutNovemberData = createAdjustedGraphs(data_from_all_days[7].iloc[0:20300], 20300, "26. November")

digitizedNovemberData = modifyPressureGraph()
digitizedNovemberData[0] = digitizedNovemberData[0][(digitizedNovemberData[0] != 0).all(1)] # Fjerner nullene 


if __name__ == "__main__":    # Dersom skriptet bli kalt på fra et annet skript vil ikke følgende kode kjøres
    
    PlotDay(digitizedNovemberData, 0, "Pressure", False, floorLevels, "26. November")
    
    print(digitizedNovemberData[0].describe())
    # Her ser vi at medianen er 1013.95, altså etasje 2
    print(digitizedNovemberData[0]["Pressure"].value_counts())
    # Her kan vi telle antall datapunkt heisa har på ulike nivå. Slik kan vi se hvilke etasjer heisen tilbringer mest tid i.
    # Om vi kunne fått renere data kunne vi og funnet ut hvilken heisturer som er mest populære.
    # Vi kunne og estimert strømforbruken til heisa.











