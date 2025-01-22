from pathlib import Path
import datetime as dt
import pandas as pd
import numpy as np
import streamlit as st

PRAEFIX = "https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ6/fz6_"
SUFFIX = "?__blob=publicationFile"
blatt = "FZ 6.1"
kopfzeile = 7
herstellerspalte = "Herstellerklartext"
typspalte = "Handelsname"
hsnspalte = "Hersteller-\nschlüssel-\nnummer"
tsnspalte = "Typ-\nschlüssel-\nnummer"
wertspalte = "Anzahl"
aktjahr = int(dt.date.today().strftime("%Y"))

@st.cache_data  # 👈 Add the caching decorator
def daten_laden():
    
    urls = [PRAEFIX + str(aktjahr) + ".xls" + SUFFIX, PRAEFIX + str(aktjahr) + ".xlsx" + SUFFIX, PRAEFIX + str(aktjahr-1) + ".xls" + SUFFIX, PRAEFIX + str(aktjahr-1) + ".xlsx" + SUFFIX]
    i=0
    df = pd.read_excel(urls[2], sheet_name=blatt, header=kopfzeile)
    ##while i < 4:
       ## try: 
            
        ##except:
        ##    i=i+1
        ##else:
        ##    i=5
   ## return
        
    df = df.drop(df.columns[[0]], axis=1)
    df = df[~df[wertspalte].isna()]
    df = df.fillna("");
    df[wertspalte] = df[wertspalte].astype("int32")
    df[herstellerspalte] = df[herstellerspalte].astype("category")
    df[hsnspalte] = df[hsnspalte].astype("category")
    df[tsnspalte] = df[tsnspalte].astype("category")
    df = df.rename(columns={herstellerspalte: "Hersteller", typspalte : "Typ", hsnspalte: "HSN", tsnspalte : "TSN"})
    
    return df

df = daten_laden()

st.write("""
# Fahrzeugbestand nach Herstellern und Typen
Datenstand *Januar 2024*
""")

herstellersuche = ""
typsuche = ""
hsnsuche = ""
tsnsuche = ""

with st.form("suchformular"):
    st.write("Suche")
    spalte1 = st.columns([1,1])
    hsnsuche = spalte1[0].text_input("HSN")
    tsnsuche = spalte1[1].text_input("TSN")
    
    spalte2 = st.columns([1,1])
    herstellersuche = spalte2[0].text_input("Hersteller")
    typsuche = spalte2[1].text_input("Typ")
    
    st.form_submit_button("Suchen")

dff = df[df["Typ"].str.contains("(?i)" + typsuche) & df["Hersteller"].str.contains("(?i)" + herstellersuche) 
& df["HSN"].str.contains("(?i)" + hsnsuche) & df["TSN"].str.contains("(?i)" + tsnsuche)]

st.dataframe(dff, use_container_width=True, hide_index=True)
st.write("**" + str(len(dff.index)) + "** Datensätze gefunden.")
st.write("Datenquelle: Kraftfahrt-Bundesamt, Bestand nach Herstellern und Typen (FZ 6), " + dt.date.today().strftime("%d.%m.%Y") + "; [Datenlizenz by-2-0](https://www.govdata.de/dl-de/by-2-0); eigene Darstellung")


