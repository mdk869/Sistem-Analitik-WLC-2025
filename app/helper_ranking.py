import pandas as pd
import plotly.express as px
import streamlit as st
from app.helper_utils import convert_columns_to_numeric

def leaderboard_peserta(df, top_n=10):
    """
    Jana leaderboard berdasarkan % Penurunan Berat.
    """
    df = df.copy()

    # Pastikan kolum numeric
    df = convert_columns_to_numeric(df, ["BeratAwal", "BeratTerkini"])

    # Bersihkan NaN
    df[["BeratAwal", "BeratTerkini"]] = df[["BeratAwal", "BeratTerkini"]].fillna(0)

    # Kiraan % Penurunan dengan kawalan ZeroDivisionError
    df["% Penurunan"] = df.apply(
        lambda x: round(((x["BeratAwal"] - x["BeratTerkini"]) / x["BeratAwal"]) * 100, 2)
        if x["BeratAwal"] > 0 else 0,
        axis=1
    )

    df["% Penurunan"] = df["% Penurunan"].fillna(0).clip(lower=0)

    # Susun leaderboard
    df = df.sort_values(by="% Penurunan", ascending=False).reset_index(drop=True)
    df["Ranking"] = df.index + 1

    return df[["Ranking", "Nama", "NoStaf", "% Penurunan"]].head(top_n)

def trend_penurunan_bulanan(df_rekod):
    if df_rekod.empty:
        return None

    df_rekod = df_rekod.copy()
    df_rekod['Tarikh'] = pd.to_datetime(df_rekod['Tarikh'], errors='coerce')
    df_group = df_rekod.groupby("SesiBulan")["Berat"].mean().reset_index()

    fig = px.line(
        df_group, x="SesiBulan", y="Berat",
        title="Trend Berat Purata Bulanan",
        markers=True
    )

    return fig
