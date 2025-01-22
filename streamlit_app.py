from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st

datei = "fz6_2024.xls"
blatt = "FZ 6.1"
kopfzeile = 7
herstellerspalte = "Herstellerklartext"
typspalte = "Handelsname"
hsnspalte = "Hersteller-\nschlüssel-\nnummer"
tsnspalte = "Typ-\nschlüssel-\nnummer"
wertspalte = "Anzahl"

    df = pd.read_excel(datei, sheet_name=blatt, header=kopfzeile)
    df = df.drop(df.columns[[0]], axis=1)
    df = df[~df[wertspalte].isna()]
    df = df.fillna("");
    df[wertspalte] = df[wertspalte].astype("int32")
    df[herstellerspalte] = df[herstellerspalte].astype("category")
    df[hsnspalte] = df[hsnspalte].astype("category")
    df[tsnspalte] = df[tsnspalte].astype("category")

st.write("""
# My first app
Hello *world!*
""")

herstellersuche = ""
typsuche = ""
hsnsuche = ""
tsnsuche = ""

with st.form("suchformular"):
    st.write("Suche")
    hsnsuche = st.text_input("HSN")
    tsnsuche = st.text_input("TSN")
    herstellersuche = st.text_input("Hersteller")
    typsuche = st.text_input("Typ")
    st.form_submit_button("Suchen")

df[df[typspalte].str.contains("(?i)" + typsuche) & df[herstellerspalte].str.contains("(?i)" + herstellersuche) 
& df[hsnspalte].str.contains("(?i)" + hsnsuche) & df[tsnspalte].str.contains("(?i)" + tsnsuche)]
