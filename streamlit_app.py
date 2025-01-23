from pathlib import Path
import datetime as dt
import pandas as pd
import numpy as np
import streamlit as st

PRAEFIX = "https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ6/fz6_"
SUFFIX = "?__blob=publicationFile"
BLATT = "FZ 6.1"
KOPFZEILE = 7
HERSTELLERSPALTE = "Herstellerklartext"
TYPSPALTE = "Handelsname"
HSNSPALTE = "Hersteller-\nschlüssel-\nnummer"
TSNSPALTE = "Typ-\nschlüssel-\nnummer"
WERTSPALTE = "Anzahl"
AKTJAHR = int(dt.date.today().strftime("%Y"))

@st.dialog("Info")
def infodialog():
    st.write("Hier kann die Anzahl der, beim Kraftfahrt-Bundesamt, registrierten Fahrzeuge nach 4 unterschiedlichen Suchkriterien abgefragt werden. Groß- und Kleinschreibung wird nicht beachtet. Über die Checkbox 'Exakt' erhält man nur Suchergebnisse, die mit den Eingaben exakt übereinstimmen. Ansonsten werden Ergebnisse gezeigt, die die Suchkriterien beinhalten. Die Daten werden einmal pro Jahr vom KBA aktualisiert. Aktueller Datenstand ist der Januar " + str(df["Jahr"].unique()[0]) + ".")

@st.cache_data  # 👈 Add the caching decorator
def daten_laden():
    jahroffset = 0
    i = 0
    
    while i < 4:
        url = PRAEFIX
        if (i < 2):
            url = url + str(AKTJAHR)
        else:
            url = url + str(AKTJAHR-1)
            jahroffset = 1
        if (i % 2) == 0:
            url = url + ".xlsx"
        else:
            url = url + ".xls"

        url = url + SUFFIX
        
        try:
            df = pd.read_excel(url, sheet_name=BLATT, header=KOPFZEILE)
        except:
            i=i+1
        else:
            i=5
        
    df = df.drop(df.columns[[0]], axis=1)
    df = df[~df[WERTSPALTE].isna()]
    df = df.fillna("");
    df[WERTSPALTE] = df[WERTSPALTE].astype("int32")
    df[HERSTELLERSPALTE] = df[HERSTELLERSPALTE].astype("category")
    df[HSNSPALTE] = df[HSNSPALTE].astype("category")
    df[TSNSPALTE] = df[TSNSPALTE].astype("category")
    df = df.rename(columns={HERSTELLERSPALTE: "Hersteller", TYPSPALTE : "Typ", HSNSPALTE: "HSN", TSNSPALTE : "TSN"})
    df["Jahr"] = AKTJAHR - jahroffset
    df["Jahr"] = df["Jahr"].astype("category")
        
    return df

df = daten_laden()

st.write("""
# Fahrzeugbestand beim KBA
**Datenstand: Januar """ + str(df["Jahr"].unique()[0]) + """**
""")

if st.button("Info"):
    infodialog()

herstellersuche = ""
typsuche = ""
hsnsuche = ""
tsnsuche = ""

with st.form("suchformular"):
    st.write("Suche")
    spalte1, spalte2 = st.columns([1,1])
    hsnsuche = spalte1[0].text_input("HSN")
    tsnsuche = spalte1[1].text_input("TSN")
    
    #spalte2 = st.columns([1,1])
    herstellersuche = spalte2[0].text_input("Hersteller")
    typsuche = spalte2[1].text_input("Typ")
    
    st.form_submit_button("Suchen")

dff = df.drop(["Jahr"], axis=1)
dff = dff[dff["Typ"].str.contains("(?i)" + typsuche) & dff["Hersteller"].str.contains("(?i)" + herstellersuche) 
& dff["HSN"].str.contains("(?i)" + hsnsuche) & dff["TSN"].str.contains("(?i)" + tsnsuche)]

st.dataframe(dff, use_container_width=True, hide_index=True)
st.write("**" + str(len(dff.index)) + "** Datensätze gefunden") #, Gesamtsumme **" + str(dff["Anzahl"].sum()) + "**")
st.write("Datenquelle: Kraftfahrt-Bundesamt, Bestand nach Herstellern und Typen (FZ 6), " + dt.date.today().strftime("%d.%m.%Y") + "; [Datenlizenz by-2-0](https://www.govdata.de/dl-de/by-2-0); eigene Darstellung")
