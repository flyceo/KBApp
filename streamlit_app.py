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

if Path(datei.split(".")[0] + ".pkl").exists():
    pd.read_pickle(datei.split(".")[0] + ".pkl")
else:
    df = pd.read_excel(datei, sheet_name=blatt, header=kopfzeile, engine="openpyxl")
    df = df.drop(df.columns[[0]], axis=1)
    df = df[~df[wertspalte].isna()]
    df = df.fillna("");
    df[wertspalte] = df[wertspalte].astype("int32")
    df[herstellerspalte] = df[herstellerspalte].astype("category")
    df[hsnspalte] = df[hsnspalte].astype("category")
    df[tsnspalte] = df[tsnspalte].astype("category")
    df.to_pickle(datei.split(".")[0] + ".pkl")



st.write("""
# My first app
Hello *world!*
""")
