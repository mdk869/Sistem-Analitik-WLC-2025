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
    """
    Jana graf trend berat purata bulanan.
    """
    if df_rekod.empty:
        return None

    df = df_rekod.copy()

    # Tukar Tarikh ke datetime
    df["Tarikh"] = pd.to_datetime(df["Tarikh"], errors="coerce")
    df = df.dropna(subset=["Tarikh"])

    # Wujudkan kolum 'SesiBulan' contoh: 'Jun 2025'
    df["SesiBulan"] = df["Tarikh"].dt.strftime('%b %Y')

    # Convert Berat ke numeric
    df["Berat"] = pd.to_numeric(df["Berat"], errors="coerce")
    df = df.dropna(subset=["Berat"])

    # Group by bulan
    df_group = df.groupby("SesiBulan").agg(
        BeratPurata=('Berat', 'mean'),
        BilanganTimbang=('Berat', 'count')
    ).reset_index()

    # Susun ikut tarikh sebenar
    df_group["TarikhSort"] = pd.to_datetime(
        df_group["SesiBulan"], format='%b %Y', errors='coerce'
    )
    df_group = df_group.sort_values(by="TarikhSort")

    # Plot
    fig = px.line(
        df_group,
        x="SesiBulan",
        y="BeratPurata",
        markers=True,
        text="BilanganTimbang",
        title="Trend Berat Purata Bulanan"
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(
        xaxis_title="Bulan",
        yaxis_title="Berat Purata (kg)",
        showlegend=False
    )

    return fig
