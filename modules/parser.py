import pandas as pd

REQUIRED_COLUMNS = ["baseMean", "log2FoldChange", "pvalue", "padj"]
GENE_COLUMNS = ["symbol", "gene", "SYMBOL", "GENE", "Gene", "gene_name", "gene_symbol"]

def load_deseq2(filepath):
    df = pd.read_csv(filepath, index_col=0)
    df.columns = df.columns.str.strip()
    
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}. Found: {', '.join(df.columns.tolist())}")
    
    gene_col = next((c for c in GENE_COLUMNS if c in df.columns), None)
    if gene_col and gene_col != "symbol":
        df = df.rename(columns={gene_col: "symbol"})
    
    df = df.dropna(subset=["padj"])
    df["significant"] = (df["padj"] < 0.05) & (abs(df["log2FoldChange"]) > 1)
    df["direction"] = "not significant"
    df.loc[(df["log2FoldChange"] > 1) & (df["padj"] < 0.05), "direction"] = "upregulated"
    df.loc[(df["log2FoldChange"] < -1) & (df["padj"] < 0.05), "direction"] = "downregulated"
    return df
