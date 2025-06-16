# streamlit_app.py

import streamlit as st
import pandas as pd
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
st.title("📊 QK-Daten Plotter")

st.sidebar.header("1️⃣ Excel-Dateien hochladen")
vk_file = st.sidebar.file_uploader("👉 VK Test.xlsx hochladen", type=["xlsx"])
quant_file = st.sidebar.file_uploader("👉 Test quantitativ.xlsx hochladen", type=["xlsx"])

# Temporäres Einlesen nur zur Anzeige der verfügbaren Analyte
selected_analyt = None

if vk_file and quant_file:
    temp_vk = pd.read_excel(vk_file)
    temp_quant = pd.read_excel(quant_file)

    analyte = sorted(set(temp_vk['Analyt'].dropna().unique()).intersection(temp_quant['Analyt'].dropna().unique()))

    if analyte:
        selected_analyt = st.sidebar.selectbox("🔬 Analyt auswählen", analyte)
    else:
        st.warning("⚠️ Keine gemeinsamen Analyte gefunden.")

# Wenn alles bereit ist:
if vk_file and quant_file and selected_analyt:
    st.success(f"✅ Dateien geladen – Analyt: {selected_analyt}")

    # Gefilterte Daten laden
    dataVK, dataQuant = load_data_vk_quant(vk_file, quant_file, selected_analyt)

    st.header("2️⃣ Intraday Plots")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📌 Intraday QK1")
        st.plotly_chart(plot_intraday_qk1(dataVK), use_container_width=True)
    with col2:
        st.subheader("📌 Intraday QK2")
        st.plotly_chart(plot_intraday_qk2(dataVK), use_container_width=True)

    st.header("3️⃣ Interday Plots")
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("📌 Interday QK1")
        st.plotly_chart(plot_interday_qk1(dataVK), use_container_width=True)
    with col4:
        st.subheader("📌 Interday QK2")
        st.plotly_chart(plot_interday_qk2(dataVK), use_container_width=True)

    st.header("4️⃣ Methodenvergleich: Boxplot")
    st.plotly_chart(plot_boxplot_comparison(dataQuant), use_container_width=True)

    st.header("5️⃣ Methodenvergleich: Korrelation")
    st.plotly_chart(plot_correlation(dataQuant), use_container_width=True)

elif vk_file and quant_file:
    st.info("⬅️ Bitte wähle einen Analyt aus der Liste auf der linken Seite.")
else:
    st.info("⬅️ Bitte lade beide Excel-Dateien hoch, um zu starten.")