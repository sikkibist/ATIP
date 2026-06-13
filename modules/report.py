from fpdf import FPDF
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os

def save_plot_as_png(fig, filename, output_dir="output"):
    path = os.path.join(output_dir, filename)
    fig.write_image(path, width=900, height=500)
    return path

def generate_report(df, enrichment, volcano_fig, ma_fig, heatmap_fig, output_dir="output"):
    v_path = save_plot_as_png(volcano_fig, "volcano.png", output_dir)
    m_path = save_plot_as_png(ma_fig, "ma.png", output_dir)
    h_path = save_plot_as_png(heatmap_fig, "heatmap.png", output_dir)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Transcriptomic Analysis Report", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Summary Statistics", ln=True)
    pdf.set_font("Helvetica", size=11)
    sig = int(df['significant'].sum())
    up = int((df['direction']=='upregulated').sum())
    down = int((df['direction']=='downregulated').sum())
    pdf.cell(0, 7, f"Total genes analyzed: {len(df)}", ln=True)
    pdf.cell(0, 7, f"Significant DEGs (padj < 0.05, |log2FC| > 1): {sig}", ln=True)
    pdf.cell(0, 7, f"Upregulated: {up}   |   Downregulated: {down}", ln=True)
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Volcano Plot", ln=True)
    pdf.image(v_path, w=180)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "MA Plot", ln=True)
    pdf.image(m_path, w=180)
    pdf.ln(5)
    pdf.cell(0, 8, "Top 50 DEGs Heatmap", ln=True)
    pdf.image(h_path, w=180)
    for key, table in enrichment.items():
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, f"Enrichment: {key.replace('_', ' ').title()}", ln=True)
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(90, 7, "Term", border=1)
        pdf.cell(30, 7, "P-value", border=1)
        pdf.cell(35, 7, "Adj. P-value", border=1)
        pdf.cell(35, 7, "Score", border=1, ln=True)
        pdf.set_font("Helvetica", size=8)
        for _, row in table.head(15).iterrows():
            term = str(row['term'])[:55]
            pdf.cell(90, 6, term, border=1)
            pdf.cell(30, 6, str(row['pvalue']), border=1)
            pdf.cell(35, 6, str(row['adj_pvalue']), border=1)
            pdf.cell(35, 6, str(row['combined_score']), border=1, ln=True)
    report_path = os.path.join(output_dir, "report.pdf")
    pdf.output(report_path)
    return report_path
