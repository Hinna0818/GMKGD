# 🌿 GMKGD: Gut Microbiome Knowledge Graph Database


> **GMKGD** is an interactive, searchable, and expandable knowledge graph database designed to map the complex relationships between **gut microbes**, **metabolites**, **molecular targets**, **human diseases**, and **food sources**.

---

## 🧬 Overview

**GMKGD** integrates multi-omics knowledge into a structured graph model with entity types including:

- 🦠 Microbes (NCBI Taxonomy)
- 🧪 Metabolites (Chemical structure, SMILES, InChI)
- 🎯 Targets / Genes (UniProt, Gene Symbol)
- 🩺 Diseases (DOID ontology)
- 🍎 Food Sources (ingredients/nutrient content)

It supports **keyword-based search**, **interactive network visualization**, and **functional enrichment analysis** (KEGG & GO), offering a user-friendly interface for both researchers and clinicians.

---

## 🔧 Features

| Feature                        | Description |
|-------------------------------|-------------|
| 🔍 **Keyword Search**         | Multi-entity fuzzy search (e.g. "Bifidobacterium") |
| 🕸️ **Knowledge Graph**        | Interactive network built with PyVis + NetworkX |
| 📈 **Enrichment Analysis**    | Built-in KEGG & GO-BP enrichment via [GSEApy](https://github.com/zqfang/GSEApy) |
| 📊 **Statistics Dashboard**   | Distribution & Top5 rankings (e.g. most common microbes, diseases) |
| 💾 **Downloadable Results**  | CSV exports + Graph image export |

---

## 🚀 Quick Start

### 💻 Prerequisites

- Python ≥ 3.8
- MySQL ≥ 8.0
- Streamlit ≥ 1.20
- Required packages:
```bash
pip install -r requirements.txt
