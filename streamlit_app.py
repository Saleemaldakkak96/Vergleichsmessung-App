
# app.py

import streamlit as st
import pandas as pd
import numpy as np

from qk_plot_utils import (
    load_data_vk_quant,
    plot_intraday_qk1,
    plot_intraday_qk2,
    plot_interday_qk1,
    plot_interday_qk2,
    plot_boxplot_comparison,
    plot_correlation
)

st.set_page_config(page_title="QK-Daten Plotter", layout="wide")

st.title("📊 QK-Daten Plotter (aus R-Skript portiert)")

# Datei Upload
st.sidebar.header("1️⃣ Excel-Dateien hochladen")

vk_file = st.sidebar.file_uploader("👉 VK Test.xlsx hochladen", type=["xlsx"])
quant_file = st.sidebar.file_uploader("👉 Test quantitativ.xlsx hochladen", type=["xlsx"])
methode = st.sidebar.selectbox(
    "Wähle die Analysemethode",
    ["Quantitativ", "Semi-Quantitativ", "Qualitativ"]
)

# Wenn beide vorhanden:
if vk_file and quant_file:
    st.success("✅ Dateien erfolgreich geladen!")

    # Daten laden
    dataVK, dataQuant = load_data_vk_quant(vk_file, quant_file)

    # Section: Intraday Plots
    st.header("2️⃣ Intraday Plots")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Intraday QK1")
        fig_intraday_qk1 = plot_intraday_qk1(dataVK)
        st.plotly_chart(fig_intraday_qk1, use_container_width=True)

    with col2:
        st.subheader("📌 Intraday QK2")
        fig_intraday_qk2 = plot_intraday_qk2(dataVK)
        st.plotly_chart(fig_intraday_qk2, use_container_width=True)

    # Section: Interday Plots
    st.header("3️⃣ Interday Plots")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📌 Interday QK1")
        fig_interday_qk1 = plot_interday_qk1(dataVK)
        st.plotly_chart(fig_interday_qk1, use_container_width=True)

    with col4:
        st.subheader("📌 Interday QK2")
        fig_interday_qk2 = plot_interday_qk2(dataVK)
        st.plotly_chart(fig_interday_qk2, use_container_width=True)

    # Section: Methodenvergleich Boxplot
    st.header("4️⃣ Methodenvergleich: Boxplot")

    fig_boxplot = plot_boxplot_comparison(dataQuant)
    st.plotly_chart(fig_boxplot, use_container_width=True)

    # Section: Methodenvergleich Korrelation
    st.header("5️⃣ Methodenvergleich: Korrelation Plot")

    fig_correlation = plot_correlation(dataQuant)
    st.plotly_chart(fig_correlation, use_container_width=True)

else:
    st.info("⬅️ Bitte lade beide Excel-Dateien hoch, um die Plots zu sehen.")

