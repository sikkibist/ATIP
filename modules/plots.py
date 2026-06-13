import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def volcano_plot(df):
    df = df.copy()
    df['-log10padj'] = -np.log10(df['padj'].clip(lower=1e-300))
    color_map = {'upregulated':'red','downregulated':'blue','not significant':'grey'}
    fig = px.scatter(df, x='log2FoldChange', y='-log10padj', color='direction',
        color_discrete_map=color_map,
        hover_data=['symbol'] if 'symbol' in df.columns else None,
        title='Volcano Plot',
        labels={'log2FoldChange':'log2 Fold Change','-log10padj':'-log10(padj)'})
    fig.add_hline(y=-np.log10(0.05), line_dash='dash', line_color='black')
    fig.add_vline(x=1, line_dash='dash', line_color='black')
    fig.add_vline(x=-1, line_dash='dash', line_color='black')
    return fig.to_html(full_html=False)

def ma_plot(df):
    df = df.copy()
    df['log10baseMean'] = np.log10(df['baseMean'].clip(lower=1e-10))
    color_map = {'upregulated':'red','downregulated':'blue','not significant':'grey'}
    fig = px.scatter(df, x='log10baseMean', y='log2FoldChange', color='direction',
        color_discrete_map=color_map,
        title='MA Plot',
        labels={'log10baseMean':'log10(baseMean)','log2FoldChange':'log2 Fold Change'})
    fig.add_hline(y=0, line_dash='dash', line_color='black')
    return fig.to_html(full_html=False)

def heatmap_top50(df):
    up = df[df['direction']=='upregulated'].nsmallest(25,'padj')
    down = df[df['direction']=='downregulated'].nsmallest(25,'padj')
    top50 = pd.concat([up, down])
    gene_col = 'symbol' if 'symbol' in df.columns else df.columns[0]
    fig = go.Figure(data=go.Heatmap(
        z=top50['log2FoldChange'].values.reshape(-1,1),
        y=top50[gene_col].values,
        x=['log2FC'],
        colorscale='RdBu_r',
        zmid=0))
    fig.update_layout(title='Top 50 DEGs Heatmap', height=800)
    return fig.to_html(full_html=False)
