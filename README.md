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
#### Required tools
- Python ≥ 3.8
- MySQL ≥ 8.0
- Streamlit ≥ 1.20

#### Required packages:
- streamlit>=1.25
- pandas>=1.5
- sqlalchemy>=2.0
- pymysql>=1.0
- networkx>=2.8
- pyvis>=0.3.2
- altair>=4.2
- matplotlib>=3.5
- gseapy>=1.0
- plotly>=5.10

### 📦 Requirements
We recommend using conda to manage your Python environment to ensure compatibility and avoid dependency issues.
```bash
# Step 1: Create a new conda environment
conda create -n gmkgd_env python=3.9

# Step 2: Activate the environment
conda activate gmkgd_env

# Step 3: Install required packages
pip install -r requirements.txt
```

Alternatively, if you are using venv or virtualenv, make sure you install the dependencies using:
```{bash}
pip install -r requirements.txt
```

### 📥 Step 1. Download files
Download **./SQL/gutdb/sql** for initializing database

### 🧰 Step 2. Add database into your computer
```bash
mysql -u root -p < gutdb.sql
```

### 🚀 Step 3. Launch the Application
Navigate to the project directory where **main.py** is located, and run the Streamlit application:
```bash
streamlit run GMKGD/main.py
```
By default, it will open at: http://localhost:8501

### 🗂 Project Structure
```{graphql}
GMKGD/
│
├── Python/                  # Main app source code
│   ├── main.py            # Entry point of the application
│   ├── init.py            # Database connection initialization
│   ├── query.py           # Query engine and SQL logic
│   ├── enrichment.py      # KEGG and GO enrichment module
│   ├── network_viz.py     # Interactive network visualization
│   ├── sankey_plot.py     # Sankey diagram visualization
│   ├── dashboard.py       # Homepage and dashboard logic
│   └── config.py          # Color palette and settings
│
├── SQL/               
│   └── gutdb.sql
├── requirements.txt       # Python dependency list
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
```

### ⚙️ Database Configuration
Ensure your MySQL server is running and the database gutdb is created with the correct schema. Update the MySQL connection in **config.py**:
```{python}
engine = create_engine("mysql+pymysql://<username>:<password>@localhost:3306/gutdb?charset=utf8mb4")

## example
# engine = create_engine("mysql+pymysql://hinna:hinna12345@localhost:3306/gutdb?charset=utf8mb4")
```




