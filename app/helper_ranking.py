import pandas as pd
import plotly.express as px
import streamlit as st


def leaderboard_peserta(df, top_n=10):
    df = df.copy()
    df["% Penurunan"] = ((df["BeratAwal"] - df["BeratTerkini"]) / df["BeratAwal"] * 100).round(2)
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
