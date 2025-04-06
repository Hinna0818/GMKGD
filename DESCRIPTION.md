# 📘 GMKGD - Description (v1.0.1)

## Project: GMKGD (Gut Microbiome Knowledge Graph Database)

### Version: 1.0 (Initial Release)
####  Version: 1.0.1 (2025.4.6 Release)

---

## 🔍 Summary

**GMKGD** is a version 1.0 release of a structured knowledge graph database designed to capture and explore the complex relationships between **gut microbiota**, **metabolites**, **targets**, **diseases**, and **food sources**.

This version introduces a **local and interactive web-based platform**, allowing users to perform **query-based exploration**, **network visualization**, and **enrichment analysis** (KEGG & GO). The database is implemented with MySQL backend and Streamlit frontend, and the data has been manually curated from multiple public resources.

---

## ✅ Included in this Version

- **Database schema**: 5 core entities (Microbes, Metabolites, Targets, Diseases, Food) + 4 association tables.
- **Streamlit frontend** with:
  - Keyword-based query
  - Interactive network graph (PyVis + NetworkX)
  - KEGG/GO enrichment using GSEApy
  - Downloadable tables and plots
- **Statistics dashboard**:
  - Entity counts
  - Microbe rank distribution
  - Top 5 frequency barplots (microbe, disease, gene, metabolite)

---

## 🔧 Technologies

- Backend: `MySQL`, `SQLAlchemy`
- Frontend: `Streamlit`, `PyVis`, `Altair`, `Matplotlib`
- Enrichment Analysis: `GSEApy` (Enrichr API)

---

## 🚧 Limitations (v1.0)

- Database runs **locally only**
- Food-microbe interactions are limited and manually annotated
- No API or multi-user access support yet
- No automatic data update pipeline
- No support for **dynamic updates**, **literature mining**, or **user uploads**

---

## 🔮 Planned in Future Releases

- 🌐 **Cloud deployment** and public access (Streamlit Cloud / Docker / Heroku)
- 🔁 **Automated data updates** via external APIs (e.g., UniProt, PubChem, DO)
- 🔎 **NLP-based relation mining** from PubMed abstracts
- 👥 **User annotation & submission module**
- 📈 **Quantitative analysis tools** (expression data, abundance profiling)
- 📊 More advanced visualizations (e.g., Sankey diagrams, co-occurrence networks)

---

## 📅 Release Note

- **v1.0** (2025.4.3): First functional and interactive version of GMKGD.
  - Focus on manually curated knowledge
  - Basic search & visualization modules completed
  - Enrichment analysis (KEGG + GO) integrated

- **v1.0.1** (2025.4.6): Supplementary version of GMKGD1.0.
  - Add Sankey-plot for microbe-metabolites-targets visualization
  - Fix bugs
  - Support Key words query

---

## 📬 Contact

For suggestions, collaborations, or dataset contributions:  
📧 `hinna@i.smu.edu.cn`  
GitHub: [github.com/Hinna0818/GMKGD](https://github.com/Hinna0818/GMKGD)

