# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 15:59:57 2020

@author: fredr
"""
#oppgaver:
import pandas as pd
import numpy as np
#%%
#1:

#importerer datafilen:
df_opg1 = pd.read_csv('Datasets/Weather/2342202.csv')

#%%
#2:
# ser at dataen er organisert i 92099 rader og fem kolonner: Station, Name, Date og TAVG
# Datasettet består av datatypene "object" og "float64".
head = df_opg1.head()
info = df_opg1.info()

#%%
#3:
df_opg1.drop_duplicates(inplace=True) # Dropper duplikerte rader
df_opg1.dropna(inplace=True) # Dropper rader med null-verdier
df_opg1.reset_index(inplace=True) # Lager en ny kolonne med indexer som stemmer
del df_opg1["index"] # Sletter kolonnen med indexer som ikke stemte 

df_opg1.info() 
# Ser at det nå kun er 7606 rader igjen i datasettet, til tross for at det var 92099 rader til å begynne med.
# Dette er fordi at en stor majoritet av radene til å begynne med inneholdt null-verdier.  

#%%
#4:
# Splitter kolonnen med hensyn på komma.
# Det gir en "Series" med to kolonner, hvor første kolonne [0] er area, og andre kolonne [1] er country.
area = df_opg1["NAME"].str.split(',', expand=True)[0]
country_and_city = df_opg1["NAME"].str.split(',', expand=True)[1]

# Setter så inn kolonnene i dataframen:
df_opg1["AREA"] = area
df_opg1["COUNTRY"] = country_and_city
# Og sletter den originale kolonnen NAME
del df_opg1["NAME"]

#%%
#5:
# Vi har allerede en "Series" country_and_city som vi kan dele opp. 
# Vi splitter den kun en gang (n=1) fra høyre side (ergo "rsplit" istedet for "split") med hensyn på mellomrom. 
# Vi splitter fra høyre slik at radene som kun inneholder "country" og ikke "city" kommer i riktig kolonne.
city = country_and_city.str.rsplit(' ', expand=True, n=1)[0] #alle byene
country = country_and_city.str.rsplit(' ', expand=True, n=1)[1] #alle landene

# Setter alle landene og byene inn i dataframen:
df_opg1["COUNTRY"] = country
df_opg1["CITY"] = city

#6:
# Skjønner ikke hva oppgaven ber om, vi har allerede gjort country-kolonnen til landskoder på to bokstaver.

#%%
#7:
#importerer en annen datafil
df_opg7 = pd.read_csv('Datasets/Weather/2342207.csv')

#7: trinn 3 (slette nan-kolonner og duplikerte rader):
df_opg7.drop_duplicates(inplace=True) # Dropper duplikerte rader
df_opg7.dropna(inplace=True) # Dropper rader med null-verdier
df_opg7.reset_index(inplace=True) # Lager en ny kolonne med indexer som stemmer
del df_opg7["index"] # Sletter kolonnen med indexer som ikke stemte 

#7: trinn 4 og 5 (deler NAME-kolonnen i to kolonner AREA og COUNTRY):

# Lager en kolonne Area:
area = df_opg7["NAME"].str.split(',', expand=True)[0]

# Lager en kolonne som inneholder landskoder og by-koder.
country_and_city = df_opg7["NAME"].str.split(',', expand=True)[1]

# Lager så en kolonne som kun inneholder landskoder (trinn 5):
country = country_and_city.str.rsplit(' ', expand=True, n=1)[1] #alle landene

# Adder begge kolonnene til dataframen:
df_opg7["AREA"] = area
df_opg7["COUNTRY"] = country

# Sletter den opprinnelige "NAME"-kolonnen
del df_opg7["NAME"]

#%%
#8:
# Slår sammen de to tidligere df-ene fra opg 1 og opg 7:
df_opg8 = pd.concat([df_opg1, df_opg7], axis = 0)

# Fikser index-verdiene:
df_opg8.reset_index(inplace=True)
del df_opg8["index"]

#%%
#9:
# Skal kontrollere at df-en fra trinn 8 er riktig.
# For å gjøre dette kan vi sjekke at lengden på df-en fra trinn 8 er lik summen av lengden til de to tidligere df-ene.

# Sammenligner lengden på df-ene:
# Om lengden på df_opg1 + df_opg7 == lengden til df_opg8 så settes variabelen "kontroll_opg9" til "Riktig lengde".
if (len(df_opg1.index)+len(df_opg7.index) == len(df_opg8.index)):
    kontroll_opg9 = "Riktig lengde"
else:
    kontroll_opg9 = "Feil lengde"
# Vi kjører koden og leser at lengden stemmer, og kan konkludere med at df_opg8 er riktig.
    
#%%
#11:
import glob
file_paths = glob.glob("Datasets/Weather/*.csv") # Lagrer stien til alle filene i mappen "weather".
all_dfs = [pd.read_csv(path) for path in file_paths] # Importerer alle csv-filene fra mappen "weather" og lagrer dem i listen "all_dfs".


for df in all_dfs: # Kjører koden under en gang for hver df i listen all_dfs.
    # Trinn 3:
    # Gjør trinn 3 for hver df:
    df.drop_duplicates(inplace=True) # Dropper duplikerte rader
    df.dropna(inplace=True) # Dropper rader med null-verdier
    df.reset_index(inplace=True) # Lager en ny kolonne med indexer som stemmer
    del df["index"] # Sletter kolonnen med indexer som ikke stemte 
    
    # Trinn 4:
    # Splitter kolonnen med hensyn på komma.
    # Det gir en "Series" med to kolonner, hvor første kolonne [0] er area, og andre kolonne [1] er country.
    area = df["NAME"].str.split(',', expand=True)[0]
    country_and_city = df["NAME"].str.split(',', expand=True)[1]
    
    # Setter så kolonnene inn i dataframen:
    df["AREA"] = area
    df["COUNTRY"] = country_and_city
    # Og sletter den originale kolonnen NAME
    del df["NAME"]
    
    # Trinn 6:
    # Skal endre "COUNTRY"-kolonnen til å kun inneholde landskoder:
    # Lagrer først by-kodene i en egen kolonne "CITY", slik at vi ikke mister denne informasjonen
    df["CITY"] = df["COUNTRY"].str.rsplit(' ', expand=True, n=1)[0] #alle by-kodene
    
    # Endrer så "COUNTRY"-kolonnen til å kun inneholde lands-kodene:
    df["COUNTRY"] = df["COUNTRY"].str.rsplit(' ', expand=True, n=1)[1] #alle landene


