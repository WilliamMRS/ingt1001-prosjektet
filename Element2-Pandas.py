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
#skal droppe duplikerte rader og rader med null-verdier, og etterpå fikse index-verdiene

def fix_index(df): #lager først en funksjon som fikser index-verdiene:
    df.reset_index(inplace=True) # Lager en ny kolonne med indexer som stemmer
    del df["index"] # Sletter kolonnen med indexer som ikke stemte 
    
def trinn3(df): #lager så en funksjon som dropper duplikerte rader og rader med null-verdier:
    df.drop_duplicates(inplace=True) # Dropper duplikerte rader
    df.dropna(inplace=True) # Dropper rader med null-verdier
    fix_index(df)

trinn3(df_opg1)
df_opg1.info() 
# Ser at det nå kun er 7606 rader igjen i datasettet, til tross for at det var 92099 rader til å begynne med.
# Dette er fordi at en stor majoritet av radene til å begynne med inneholdt null-verdier.  

#%%
#4:
def trinn4(df):
    # Splitter "NAME" kolonnen med hensyn på komma.
    # Det gir en "Series" med to kolonner, hvor første kolonne [0] er area, og andre kolonne [1] er country.
    area = df["NAME"].str.split(',', expand=True)[0]
    country_and_city = df["NAME"].str.split(',', expand=True)[1]
    
    # Setter så inn kolonnene i dataframen:
    df["AREA"] = area
    df["COUNTRY"] = country_and_city
    # Og sletter den originale kolonnen NAME
    del df["NAME"]
trinn4(df_opg1)

#%%
#5:

def trinn5(df):
    # Vi skal dele opp "COUNTRY"-kolonnen i to kolonner CITY og COUNTRY
    # Vi splitter den kun en gang (n=1) fra høyre side (ergo "rsplit" istedet for "split") med hensyn på mellomrom. 
    # Vi splitter fra høyre slik at radene som kun inneholder "country" og ikke "city" kommer i riktig kolonne.
    city = df["COUNTRY"].str.rsplit(' ', expand=True, n=1)[0] #alle byene
    country = df["COUNTRY"].str.rsplit(' ', expand=True, n=1)[1] #alle landene
    
    # Setter alle lands -og by-kodene inn i dataframen:
    df["COUNTRY"] = country
    df["CITY"] = city
trinn5(df_opg1)

#%%
#6:
def trinn6(df):  #bruker COUNTRY-kolonnen fra opg 4.
    df["COUNTRY"] = df["COUNTRY"].str.rsplit(' ', expand=True, n=1)[1] # Kun landskoder

#%%
#7:
#importerer en annen datafil
df_opg7 = pd.read_csv('Datasets/Weather/2342207.csv')

#7 trinn 3 (slette nan-kolonner og duplikerte rader):
trinn3(df_opg7)

#7 trinn 4:
trinn4(df_opg7)

#7 trinn 6:
trinn6(df_opg7)

#%%
#8:
# Slår sammen de to tidligere df-ene fra opg 1 og opg 7:
df_opg8 = pd.concat([df_opg1, df_opg7], axis = 0)

# Fikser index-verdiene:
fix_index(df_opg8)

#%%
#9:
# Skal kontrollere at df-en fra trinn 8 er riktig.
# For å gjøre dette kan vi sjekke at lengden på df-en fra trinn 8 er lik summen av lengdene til de to tidligere df-ene.

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
    trinn3(df)
    
    # Trinn 4:
    trinn4(df)
    
    # Trinn 6:
    trinn6(df)
    
#%%
#12:
df_trondheim = pd.read_csv('Datasets/Weather/extra/Trondheim.csv')
# Trinn 3:
trinn3(df_trondheim)

# Trinn 4:
trinn4(df_trondheim)

# Trinn 6:
trinn6(df_trondheim)

#%%
#13: 
# Lager en ny kolonne TAVG som er gjennomsnittet av TMIN og TMAX:
df_trondheim["TAVG"] = (df_trondheim["TMIN"]+df_trondheim["TMAX"])/2

#%%
#14:
# Endrer df_trondheim slik at rekkefølgen er lik rekkefølgen til de andre df-ene, og slik at "TMIN" og "TMAX" ikke blir med.
df_trondheim = df_trondheim[["STATION", "DATE", "TAVG", "AREA", "COUNTRY"]]

#%%
#15:
# Skal kombinere alle df-ene til en supermega-df kalt df_complete

# Lager først en df_complete med alle df-ene untatt trondheim:
df_complete = pd.concat(all_dfs, axis = 0)

# Legger så trondheim df-en til i df_complete:
df_complete = pd.concat([df_complete, df_trondheim], axis = 0)

# Og fikser så index-verdiene:
fix_index(df_complete)


#%%
#16:
df_country_continent = pd.read_csv('Datasets/countryContinent.csv', encoding="iso_8859_1")

#%%
#17:
country_continent_head = df_country_continent.head(10)

# Ser at df_country_continent er strukturert i 9 kolonner. 
# Kolonnene inneholder informasjon om land, som hvilke region de befinner seg i og regions-koden og lands-koden osv. 
# Blant all denne informasjonen er det mye som kan være unyttig når vi skal se på temperaturdata
# Det som kan være nyttig å vite derimot er: land, lands-kode, kontinent og region. Fordi denne informasjonen er relevant til temperaturdataen.

#%%
#18:
# Bruker "merge" funksjonen til å slå sammen "df_complete" og "df_country_continent" til en df "df_complete_cont".
# Slår de sammen med hensyn på kolonnene "COUNTRY" (fra "df_complete") og "code_2" (fra "df_country_continent"), fordi disse kolonnene samsvarer.
df_complete_cont = pd.merge(df_complete, df_country_continent, left_on="COUNTRY", right_on="code_2")

#%%
#19:
# Dropper først "code_2" kolonnen:
del df_complete_cont["code_2"]

# Gir nye navn til de andre forespurte kolonnene:
df_complete_cont.rename(columns={"COUNTRY":"Country-code", "continent":"Continent", "country":"Country"}, inplace=True)

#%%
#21:
def column_values(df, column): # Returnerer alle unike verdier fra en spesifikk kolonne i en dataframe:
    unique_values = list(df[column].sort_values().unique())
    return unique_values
    
countries_in_df = column_values(df_complete_cont, "Country")
continents_in_df = column_values(df_complete_cont, "Continent")

#%%
#22:
def c_to_f(degrees_in_c):
    degrees_in_f = degrees_in_c * (9/5) + 32
    return degrees_in_f
df_complete_cont["TAVG"] = c_to_f(df_complete_cont["TAVG"])

