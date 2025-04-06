# enrichment.py
import streamlit as st
import gseapy as gp
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import base64
import networkx as nx
from pyvis.network import Network

def enrich_kegg_and_go(df):
    if 'Gene_symbol' not in df.columns:
        return

    gene_list = df['Gene_symbol'].dropna().unique().tolist()
    if not gene_list:
        return

    # Run Enrichment
    enr_kegg = gp.enrichr(gene_list=gene_list, gene_sets='KEGG_2021_Human', organism='Human', outdir=None, cutoff=0.1)
    enr_go = gp.enrichr(gene_list=gene_list, gene_sets='GO_Biological_Process_2021', organism='Human', outdir=None, cutoff=0.1)

    # ---------- KEGG ----------
    if enr_kegg.results is not None and not enr_kegg.results.empty:
        enr_kegg.results['GeneRatio'] = enr_kegg.results['Overlap'].apply(lambda x: int(x.split('/')[0]) / int(x.split('/')[1]))
        enr_kegg.results.sort_values("GeneRatio", ascending=False, inplace=True)

        st.markdown("### 🧬 KEGG Pathway Enrichment")
        st.dataframe(enr_kegg.results[['Term', 'Adjusted P-value', 'GeneRatio', 'Genes']], use_container_width=True)
        st.download_button("📥 下载 KEGG 结果", data=enr_kegg.results.to_csv(index=False), file_name="KEGG_enrichment.csv")

        selected = st.multiselect("选择可视化的 KEGG 通路", enr_kegg.results['Term'].tolist(), default=enr_kegg.results['Term'].tolist()[:10])
        subset = enr_kegg.results[enr_kegg.results['Term'].isin(selected)]

        _plot_bar_dot(subset, "KEGG", color="#4fc3f7")
        _plot_network(subset, "kegg_network.html")

    # ---------- GO ----------
    if enr_go.results is not None and not enr_go.results.empty:
        enr_go.results['GeneRatio'] = enr_go.results['Overlap'].apply(lambda x: int(x.split('/')[0]) / int(x.split('/')[1]))
        enr_go.results.sort_values("GeneRatio", ascending=False, inplace=True)

        st.markdown("### 🧬 GO Biological Process Enrichment")
        st.dataframe(enr_go.results[['Term', 'Adjusted P-value', 'GeneRatio', 'Genes']], use_container_width=True)
        st.download_button("📥 下载 GO 结果", data=enr_go.results.to_csv(index=False), file_name="GO_enrichment.csv")

        selected = st.multiselect("选择可视化的 GO 条目", enr_go.results['Term'].tolist(), default=enr_go.results['Term'].tolist()[:10])
        subset = enr_go.results[enr_go.results['Term'].isin(selected)]

        _plot_bar_dot(subset, "GO", color="#f4a261")
        _plot_network(subset, "go_network.html")

def _plot_bar_dot(df, label, color="#4fc3f7"):
    c1, c2 = st.columns(2)
    with c1:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            plt.figure(figsize=(10, 8))
            plt.barh(df['Term'], df['GeneRatio'], color=color)
            plt.xlabel("Gene Ratio")
            plt.title(f"{label} Barplot")
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig(tmpfile.name)
            with open(tmpfile.name, "rb") as f:
                img_data = f.read()
        st.markdown(f"<img src='data:image/png;base64,{base64.b64encode(img_data).decode()}' width='500'/>", unsafe_allow_html=True)
        st.download_button(f"下载 {label} Barplot", img_data, file_name=f"{label.lower()}_barplot.png", mime="image/png")

    with c2:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            plt.figure(figsize=(10, 8))
            plt.scatter(df['GeneRatio'], df['Term'],
                       s=df['GeneRatio'] * 800,
                       c=df['Adjusted P-value'], cmap='coolwarm', alpha=0.8, edgecolors='k')
            plt.xlabel("Gene Ratio")
            plt.title(f"{label} Dotplot")
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig(tmpfile.name)
            with open(tmpfile.name, "rb") as f:
                img_data = f.read()
        st.markdown(f"<img src='data:image/png;base64,{base64.b64encode(img_data).decode()}' width='500'/>", unsafe_allow_html=True)
        st.download_button(f"下载 {label} Dotplot", img_data, file_name=f"{label.lower()}_dotplot.png", mime="image/png")

def _plot_network(df, filename):
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_node(row['Term'], color="#81c784", label=row['Term'])
        for gene in row['Genes'].split(";"):
            G.add_node(gene, color="#ef5350", label=gene)
            G.add_edge(row['Term'], gene)

    net = Network(height="500px", width="100%")
    net.from_nx(G)
    net.save_graph(filename)

    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=600)
    st.download_button(f"下载 {filename}", data=html, file_name=filename, mime="text/html")
