# qk_plot_utils.py

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Laden und Vorbereiten der Daten
def load_data_vk_quant(vk_file, quant_file):
    dataVK = pd.read_excel(vk_file)
    dataQuant = pd.read_excel(quant_file)

    # Clean VK Daten
    for col in ['intraday1', 'intraday2', 'interday1', 'interday2']:
        dataVK[col] = pd.to_numeric(dataVK[col].astype(str).str.replace(",", "."), errors='coerce')

    # nummer_intra Spalte korrekt erzeugen
    dataVK['nummer_intra'] = np.nan
    dataVK.loc[~dataVK['intraday1'].isna(), 'nummer_intra'] = np.arange(1, dataVK['intraday1'].notna().sum() + 1)

    # nummer_inter Spalte korrekt erzeugen
    dataVK['nummer_inter'] = np.nan
    dataVK.loc[~dataVK['interday1'].isna(), 'nummer_inter'] = np.arange(1, dataVK['interday1'].notna().sum() + 1)

    # Clean quant Daten
    for col in ['Ergebnis1', 'Ergebnis2']:
        dataQuant[col] = pd.to_numeric(dataQuant[col].astype(str).str.replace(",", "."), errors='coerce')

    dataQuant = dataQuant.dropna(subset=['Ergebnis1', 'Ergebnis2'])
    dataQuant['Anzahl_im_Vgl'] = np.arange(1, len(dataQuant) + 1)

    return dataVK, dataQuant

# Helper: allgemeine QK Plot Funktion
def plot_qk(dataVK, nummer_col, value_col, zielwert, zielmin, zielmax, name_label, einheit, title):
    nummer = dataVK[nummer_col]
    value = dataVK[value_col]

    min_x = nummer.min()
    max_x = nummer.max()
    start_x = min_x - 0.5
    end_x = max_x + 0.5

    min_y = zielmin - (zielmax - zielmin) * 0.5
    max_y = zielmax + (zielmax - zielmin) * 0.5

    # Plotly Plot
    fig = go.Figure()

    # Zielbereich als Rechteck
    fig.add_shape(
        type="rect",
        x0=start_x, x1=end_x,
        y0=zielmin, y1=zielmax,
        line=dict(color="grey"),
        fillcolor="lightgrey",
        opacity=0.2,
        layer="below"
    )

    # Punkte
    fig.add_trace(go.Scatter(
        x=nummer,
        y=value,
        mode='markers',
        marker=dict(size=10, color='blue'),
        name='Messwerte'
    ))

    # Zielwert und Grenzen
    fig.add_hline(y=zielwert, line_color='black')
    fig.add_hline(y=zielmin, line_dash='dash', line_color='black')
    fig.add_hline(y=zielmax, line_dash='dash', line_color='black')

    # Layout
    fig.update_layout(
        title=title,
        xaxis_title="Messung Nr.",
        yaxis_title=f"{name_label} ({einheit})",
        xaxis=dict(range=[start_x, end_x], dtick=1),
        yaxis=dict(range=[min_y, max_y]),
        template='simple_white'
    )

    return fig

# Intraday QK1
def plot_intraday_qk1(dataVK):
    zielwert = dataVK['zielwert1'][0]
    zielmin = dataVK['zielmin1'][0]
    zielmax = dataVK['zielmax1'][0]
    name_label = dataVK['name1'][0]
    einheit = dataVK['einheit'][0]
    return plot_qk(dataVK, 'nummer_intra', 'intraday1', zielwert, zielmin, zielmax, name_label, einheit, "Intraday QK1")

# Intraday QK2
def plot_intraday_qk2(dataVK):
    zielwert = dataVK['zielwert2'][0]
    zielmin = dataVK['zielmin2'][0]
    zielmax = dataVK['zielmax2'][0]
    name_label = dataVK['name2'][0]
    einheit = dataVK['einheit'][0]
    return plot_qk(dataVK, 'nummer_intra', 'intraday2', zielwert, zielmin, zielmax, name_label, einheit, "Intraday QK2")

# Interday QK1
def plot_interday_qk1(dataVK):
    zielwert = dataVK['zielwert1'][0]
    zielmin = dataVK['zielmin1'][0]
    zielmax = dataVK['zielmax1'][0]
    name_label = dataVK['name1'][0]
    einheit = dataVK['einheit'][0]
    return plot_qk(dataVK, 'nummer_inter', 'interday1', zielwert, zielmin, zielmax, name_label, einheit, "Interday QK1")

# Interday QK2
def plot_interday_qk2(dataVK):
    zielwert = dataVK['zielwert2'][0]
    zielmin = dataVK['zielmin2'][0]
    zielmax = dataVK['zielmax2'][0]
    name_label = dataVK['name2'][0]
    einheit = dataVK['einheit'][0]
    return plot_qk(dataVK, 'nummer_inter', 'interday2', zielwert, zielmin, zielmax, name_label, einheit, "Interday QK2")

# Methodenvergleich Boxplot
def plot_boxplot_comparison(dataQuant):
    x_lab = dataQuant['NameMethode1'].iloc[0]
    y_lab = dataQuant['NameMethode2'].iloc[0]
    meth = dataQuant['Analyt'].iloc[0]
    einheit = dataQuant['Einheit'].iloc[0]

    df_long = pd.melt(dataQuant, value_vars=['Ergebnis1', 'Ergebnis2'], var_name='Methode', value_name='Wert')
    df_long['Methode'] = df_long['Methode'].map({'Ergebnis1': x_lab, 'Ergebnis2': y_lab})

    fig = px.box(df_long, x='Methode', y='Wert', color='Methode',
                 labels={'Wert': f'{meth} ({einheit})'},
                 title='Methodenvergleich: Boxplot')

    fig.update_layout(showlegend=False, template='simple_white')
    return fig

# Methodenvergleich Korrelation Plot
def plot_correlation(dataQuant):
    x = dataQuant['Ergebnis1']
    y = dataQuant['Ergebnis2']

    x_lab = dataQuant['NameMethode1'].iloc[0]
    y_lab = dataQuant['NameMethode2'].iloc[0]
    meth = dataQuant['Analyt'].iloc[0]
    einheit = dataQuant['Einheit'].iloc[0]

    max_value = max(x.max(), y.max())

    fig = go.Figure()

    # 1:1 Linie
    fig.add_trace(go.Scatter(
        x=[0, max_value],
        y=[0, max_value],
        mode='lines',
        line=dict(dash='dash', color='red'),
        name='1:1 Linie'
    ))

    # Messpunkte
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(size=10, color='blue'),
        name='Messwerte'
    ))

    fig.update_layout(
        title=f'Methodenvergleich: {meth} ({einheit})',
        xaxis_title=f'{meth} ({einheit}) ({x_lab})',
        yaxis_title=f'{meth} ({einheit}) ({y_lab})',
        xaxis=dict(range=[0, max_value]),
        yaxis=dict(range=[0, max_value]),
        template='simple_white'
    )

    return fig
