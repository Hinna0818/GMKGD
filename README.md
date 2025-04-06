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
| 📊 **Statistics Dashboard**   | Distribution of microbes' rank |
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
```

### 🚀 Launch the Application
Navigate to the project directory where **main.py** is located, and run the Streamlit application:
```bash
streamlit run GMKGD/main.py
```
By default, it will open at: http://localhost:8501

### 🗂 Project Structure
```{graphql}
GMKGD/
│
├── GMKGD/                  # Main app source code
│   ├── main.py            # Entry point of the application
│   ├── init.py            # Database connection initialization
│   ├── query.py           # Query engine and SQL logic
│   ├── enrichment.py      # KEGG and GO enrichment module
│   ├── network_viz.py     # Interactive network visualization
│   ├── sankey_plot.py     # Sankey diagram visualization
│   ├── dashboard.py       # Homepage and dashboard logic
│   └── config.py          # Color palette and settings
│
├── requirements.txt       # Python dependency list
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
```

### ⚙️ Database Configuration
Ensure your MySQL server is running and the database gutdb is created with the correct schema. Update the MySQL connection in **config.py**:
```{python}
engine = create_engine("mysql+pymysql://<username>:<password>@localhost:3306/gutdb?charset=utf8mb4")
## example: engine = create_engine("mysql+pymysql://hinna:hinna12345@localhost:3306/gutdb?charset=utf8mb4")
```




