import pandas as pd

def load_deseq2(filepath):
    df = pd.read_csv(filepath, index_col=0)
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['padj'])
    df['significant'] = (df['padj'] < 0.05) & (abs(df['log2FoldChange']) > 1)
    df['direction'] = 'not significant'
    df.loc[(df['log2FoldChange'] > 1) & (df['padj'] < 0.05), 'direction'] = 'upregulated'
    df.loc[(df['log2FoldChange'] < -1) & (df['padj'] < 0.05), 'direction'] = 'downregulated'
    return df
