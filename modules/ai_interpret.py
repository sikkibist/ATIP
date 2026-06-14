import os
from groq import Groq

def get_biological_interpretation(stats, enrichment, api_key, experimental_context="treatment vs control"):
    client = Groq(api_key=api_key or os.environ.get("GROQ_API_KEY", ""))
    
    up_kegg = enrichment.get("upregulated_KEGG", None)
    down_kegg = enrichment.get("downregulated_KEGG", None)
    up_go = enrichment.get("upregulated_GO", None)
    down_go = enrichment.get("downregulated_GO", None)
    
    def table_to_text(table, n=5):
        if table is None or len(table) == 0:
            return "None"
        return ", ".join(table.head(n)["term"].tolist())
    
    prompt = f"""You are an expert computational biologist.
Given the following RNA-seq differential expression results:
- Total genes analyzed: {stats["total_genes"]}
- Significant DEGs: {stats["significant"]} (padj < 0.05, |log2FC| > 1)
- Upregulated: {stats["upregulated"]}, Downregulated: {stats["downregulated"]}
- Experimental context: {experimental_context}

Top upregulated KEGG pathways: {table_to_text(up_kegg)}
Top downregulated KEGG pathways: {table_to_text(down_kegg)}
Top upregulated GO terms: {table_to_text(up_go)}
Top downregulated GO terms: {table_to_text(down_go)}

Write a concise biological interpretation (3-4 paragraphs) covering:
1. Overall transcriptomic response
2. Key biological processes activated
3. Key biological processes suppressed
4. Potential mechanistic implications

Be specific to the pathways listed. Do not hallucinate gene functions not supported by the data."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    
    return response.choices[0].message.content
