# ATIP — AI-Assisted Transcriptomic Interpretation Platform

A web-based bioinformatics tool that takes DESeq2 differential expression output and automatically produces interactive visualizations, functional enrichment analysis, AI-generated biological interpretation, and downloadable reports.

## Live Demo
🔗 [huggingface.co/spaces/sikkibist/ATIP](https://huggingface.co/spaces/sikkibist/ATIP)

Try it instantly with the built-in sample dataset (GSE290476 — human dermal fibroblasts, bleomycin-induced senescence).

## What It Does
Upload a DESeq2 output CSV and get:
- Interactive volcano plot, MA plot, and heatmap of top 50 DEGs
- Functional enrichment analysis via Enrichr (KEGG + GO Biological Process)
- Per-section enrichment downloads (CSV and DOCX)
- Downloadable PDF report with all plots and enrichment tables
- AI-generated biological interpretation powered by Groq (Llama 3.3 70B)

## Input Format
Your CSV must contain these columns:
Gene name column is auto-detected (symbol, gene, SYMBOL, gene_name, etc.).

## Thresholds
- Significant DEGs: padj < 0.05 and |log2FoldChange| > 1
- Enrichment databases: KEGG_2021_Human, GO_Biological_Process_2023

## Local Setup
```bash
git clone https://github.com/sikkibist/ATIP.git
cd ATIP
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY="your_groq_key"
python3 app.py
```
Open `http://127.0.0.1:7860`

## Tech Stack
- Backend: Python, Flask
- Visualizations: Plotly
- Enrichment: Enrichr REST API
- AI Interpretation: Groq API (Llama 3.3 70B)
- Report Generation: fpdf2, python-docx
- Deployment: Hugging Face Spaces (Docker)

## Validation Dataset
GSE290476 — Human dermal fibroblasts under bleomycin-induced therapy-related senescence.
Known biology: SASP activation, DNA damage response, ECM remodeling, cell cycle arrest.

## Developer
Ritika (Sikki) Bist — MSc Bioinformatics
GitHub: [sikkibist](https://github.com/sikkibist)
