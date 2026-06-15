import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

ENRICHR_URL = "https://maayanlab.cloud/Enrichr"

def submit_gene_list(genes, description="gene list"):
    genes_str = "\n".join(genes)
    response = requests.post(
        f"{ENRICHR_URL}/addList",
        files={"list": (None, genes_str), "description": (None, description)},
        timeout=(5, 10)
    )
    if response.status_code == 200:
        return response.json()["userListId"]
    else:
        raise Exception(f"Enrichr submission failed: {response.status_code}")

def get_enrichment(user_list_id, database="KEGG_2021_Human"):
    response = requests.get(
        f"{ENRICHR_URL}/enrich",
        params={"userListId": user_list_id, "backgroundType": database},
        timeout=(5, 10)
    )
    if response.status_code != 200:
        raise Exception(f"Enrichr enrichment failed: {response.status_code}")
    results = response.json()[database]
    rows = []
    for r in results[:20]:
        rows.append({
            "rank": r[0], "term": r[1], "pvalue": round(r[2], 5),
            "adj_pvalue": round(r[6], 5), "combined_score": round(r[4], 2),
            "genes": ", ".join(r[5])
        })
    return pd.DataFrame(rows)

def fetch_section(args):
    key, user_list_id, database = args
    try:
        return key, get_enrichment(user_list_id, database)
    except Exception as e:
        return key, None

def run_enrichment(df):
    gene_col = "symbol" if "symbol" in df.columns else df.columns[0]
    up_genes = df[df["direction"]=="upregulated"][gene_col].dropna().tolist()
    down_genes = df[df["direction"]=="downregulated"][gene_col].dropna().tolist()
    
    results = {}
    tasks = []
    
    try:
        if len(up_genes) > 0:
            up_id = submit_gene_list(up_genes, "upregulated")
            tasks.append(("upregulated_KEGG", up_id, "KEGG_2021_Human"))
            tasks.append(("upregulated_GO", up_id, "GO_Biological_Process_2023"))
        if len(down_genes) > 0:
            down_id = submit_gene_list(down_genes, "downregulated")
            tasks.append(("downregulated_KEGG", down_id, "KEGG_2021_Human"))
            tasks.append(("downregulated_GO", down_id, "GO_Biological_Process_2023"))
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(fetch_section, t): t for t in tasks}
            for future in as_completed(futures, timeout=60):
                key, table = future.result()
                if table is not None:
                    results[key] = table
    except Exception as e:
        results["error"] = str(e)
    
    return results
