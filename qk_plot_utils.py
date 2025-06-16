# qk_plot_utils.py (finale Version)

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Laden und Filtern nach Analyt
def load_data_vk_quant(vk_file, quant_file, selected_analyt):
    df_vk = pd.read_excel(vk_file)
    df_quant = pd.read_excel(quant_file)

    df_vk = df_vk[df_vk["Analyt"] == selected_analyt].copy()
    df_quant = df_quant[df_quant["Analyt"] == selected_analyt].copy()

    for col in ['intraday1', 'intraday2', 'interday1', 'interday2']:
        df_vk[col] = pd.to_numeric(df_vk[col].astype(str).str.replace(",", "."), errors='coerce')

    df_vk['nummer_intra'] = np.nan
    df_vk.loc[~df_vk['intraday1'].isna(), 'nummer_intra'] = np.arange(1, df_vk['intraday1'].notna().sum() + 1)

    df_vk['nummer_inter'] = np.nan
    df_vk.loc[~df_vk['interday1'].isna(), 'nummer_inter'] = np.arange(1, df_vk['interday1'].notna().sum() + 1)

    for col in ['Ergebnis1', 'Ergebnis2']:
        df_quant[col] = pd.to_numeric(df_quant[col].astype(str).str.replace(",", "."), errors='coerce')

    df_quant = df_quant.dropna(subset=['Ergebnis1', 'Ergebnis2'])
    df_quant['Anzahl_im_Vgl'] = np.arange(1, len(df_quant) + 1)

    return df_vk, df_quant

# Allgemeine QK Plotfunktion
def plot_qk(dataVK, nummer_col, value_col, zielwert, zielmin, zielmax, name_label, einheit, title):
    nummer = dataVK[nummer_col]
    value = dataVK[value_col]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=nummer,
        y=value,
        mode='markers+lines',
        marker=dict(color='blue', size=8),
        line=dict(color='blue', width=2),
        name='Messwerte'
    ))

    fig.add_shape(type="rect",
                  x0=nummer.min() - 0.5, x1=nummer.max() + 0.5,
                  y0=zielmin, y1=zielmax,
                  fillcolor="lightgrey",
                  opacity=0.4,
                  layer="below",
                  line_width=0)

    fig.add_hline(y=zielwert, line=dict(color='black', width=2))
    fig.add_hline(y=zielmin, line=dict(color='black', width=1, dash='dash'))
    fig.add_hline(y=zielmax, line=dict(color='black', width=1, dash='dash'))

    fig.update_layout(
        title=title,
        xaxis_title="Messung Nr.",
        yaxis_title=f"{name_label} ({einheit})",
        template="simple_white",
        xaxis=dict(dtick=1)
    )

    return fig

def plot_intraday_qk1(df):
    return plot_qk(df, 'nummer_intra', 'intraday1', df['zielwert1'].iloc[0], df['zielmin1'].iloc[0], df['zielmax1'].iloc[0], df['name1'].iloc[0], df['einheit'].iloc[0], "Intraday QK1")

def plot_intraday_qk2(df):
    return plot_qk(df, 'nummer_intra', 'intraday2', df['zielwert2'].iloc[0], df['zielmin2'].iloc[0], df['zielmax2'].iloc[0], df['name2'].iloc[0], df['einheit'].iloc[0], "Intraday QK2")

def plot_interday_qk1(df):
    return plot_qk(df, 'nummer_inter', 'interday1', df['zielwert1'].iloc[0], df['zielmin1'].iloc[0], df['zielmax1'].iloc[0], df['name1'].iloc[0], df['einheit'].iloc[0], "Interday QK1")

def plot_interday_qk2(df):
    return plot_qk(df, 'nummer_inter', 'interday2', df['zielwert2'].iloc[0], df['zielmin2'].iloc[0], df['zielmax2'].iloc[0], df['name2'].iloc[0], df['einheit'].iloc[0], "Interday QK2")

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

    fig.update_traces(marker=dict(size=6))
    fig.update_layout(showlegend=False, template='simple_white')
    return fig

def plot_correlation(dataQuant):
    x = dataQuant['Ergebnis1']
    y = dataQuant['Ergebnis2']

    x_lab = dataQuant['NameMethode1'].iloc[0]
    y_lab = dataQuant['NameMethode2'].iloc[0]
    meth = dataQuant['Analyt'].iloc[0]
    einheit = dataQuant['Einheit'].iloc[0]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(size=8, color='blue'), name='Messwerte'))
    fig.add_trace(go.Scatter(x=[0, max(x.max(), y.max())], y=[0, max(x.max(), y.max())], mode='lines', line=dict(dash='dash', color='red'), name='1:1 Linie'))

    fig.update_layout(
        title=f'Methodenvergleich: {meth} ({einheit})',
        xaxis_title=f'{meth} ({einheit}) ({x_lab})',
        yaxis_title=f'{meth} ({einheit}) ({y_lab})',
        template='simple_white'
    )

    return fig