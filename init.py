## Welcome to GMKGD
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import networkx as nx
from pyvis.network import Network
import altair as alt
import random
import gseapy as gp
import matplotlib.pyplot as plt
import tempfile
import base64
import os
import numpy as np

# ========== DATABASE ==========
engine = create_engine("mysql+pymysql://root:he040818@127.0.0.1:3306/gutdb?charset=utf8mb4")

# ========== 页面配置 ==========
st.set_page_config(page_title="GutDB • Microbiome Explorer", layout="wide")

# ========== 仪表盘逻辑 ==========
def show_dashboard():
    st.markdown("""
    <div style='background-color:#dcedc8; padding:1.5rem; border-radius:10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align:center;'>
        <img src='https://img.icons8.com/emoji/96/seedling.png' width='60'/>
        <h1 style='color:#2e7d32;'>🌿 GMKGD: Gut Microbiome Knowledge Graph Database</h1>
        <p style='font-size:18px; color:#333;'>
            Explore relationships between gut microbes, metabolites, targets, diseases, and food sources.<br>
            Enabling biomedical insights via interactive network exploration.
        </p>
        <div style='font-size:14px; color:#555;'>Powered by Streamlit & MySQL</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

    def count_table(table):
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            return list(result)[0][0]

    col1, col2, col3, col4, col5 = st.columns(5)
    #col4, col5 = st.columns(2)
    col1.metric("🧬 Microbes", count_table("Microbes"))
    col2.metric("🧪 Metabolites", count_table("Metabolites"))
    col3.metric("🎯 Targets", count_table("Targets"))
    col4.metric("🩺 Diseases", count_table("Diseases"))
    col5.metric("🍎 Foods", count_table("FoodSources"))

    # ========== 示例微生物分类可视化 ==========
    with engine.connect() as conn:
        micro_df = pd.read_sql("SELECT GM_Rank, COUNT(*) AS count FROM Microbes GROUP BY GM_Rank", conn)

    if not micro_df.empty:
        st.markdown("""
        <h4 style='color:#388e3c; margin-top:2rem;'>🧬 Microbe Rank Distribution</h4>
        """, unsafe_allow_html=True)
        rank_keyword = st.text_input("模糊搜索微生物等级", "")
        max_count = int(micro_df['count'].max()) if not micro_df.empty else 1
        min_micro_count = st.slider("数量阈值", 1, max_count, 1, key="micro")
        filtered_micro = micro_df[micro_df['count'] >= min_micro_count]
        if rank_keyword:
            filtered_micro = filtered_micro[filtered_micro['GM_Rank'].str.contains(rank_keyword, case=False)]

        chart = alt.Chart(filtered_micro).mark_bar(size=18, color='#4fc3f7').encode(
            y=alt.Y('GM_Rank:N', sort='-x', title='Rank'),
            x=alt.X('count:Q', title='数量'),
            tooltip=['GM_Rank', 'count']
        ).properties(height=300).configure_axis(
            labelFontSize=13,
            titleFontSize=14
        )
        st.altair_chart(chart, use_container_width=True)

    st.markdown("""
    <hr style='margin-top:2rem; margin-bottom:1rem;'>
    <h4 style='color:#388e3c;'>📘 数据库说明</h4>
    <ul style='font-size:15px;'>
        <li>覆盖微生物、代谢物、靶点、疾病和食物五大模块。</li>
        <li>支持多实体关键词模糊查询和图谱可视化。</li>
        <li>内嵌KEGG与GO_BP富集分析，全面解读代谢物靶点。</li>
        <li>查询与分析结果支持下载。</li>
    </ul>
    """, unsafe_allow_html=True)

    if st.button("🚀 前往图谱查询", type="primary"):
        st.session_state.show_query = True
        st.query_params["show_query"] = "1"

# ========== 页面路由 ==========
if "show_query" not in st.session_state:
    st.session_state.show_query = False
if st.session_state.show_query:
    if st.button("🔙 返回首页"):
        st.session_state.show_query = False
if not st.session_state.show_query:
    show_dashboard()
    st.stop()

# ========== 查询设置 ==========
st.sidebar.header("🔎 查询设置")
query_type = st.sidebar.selectbox("请选择查询类型", ["微生物", "代谢物", "靶点", "病症", "食物"])

@st.cache_data
def get_keywords_by_type(qtype):
    table_map = {
        "微生物": ("Microbes", "GM_name"),
        "代谢物": ("Metabolites", "metabolite_name"),
        "靶点": ("Targets", "gene_symbol"),
        "病症": ("Diseases", "disease_name"),
        "食物": ("FoodSources", "food_name"),
    }
    table, column = table_map[qtype]
    with engine.connect() as conn:
        sql = text(f"SELECT DISTINCT {column} FROM {table} ORDER BY {column}")
        return [row[0] for row in conn.execute(sql)]

keywords = st.sidebar.multiselect("关键词（支持多选）", get_keywords_by_type(query_type))
search_btn = st.sidebar.button("🚀 开始查询")

if search_btn and keywords:
    color_palette = ["#81c784", "#aed581", "#ffd54f", "#ffb74d", "#4fc3f7", "#9575cd", "#e57373"]
    center_colors = {kw: random.choice(color_palette) for kw in keywords}
    node_colors = {
        "Microbe": "#90caf9", "Metabolite": "#f4a261", "Target": "#4fc3f7",
        "Disease": "#ef5350", "Food": "#ffd54f"
    }

    # ========== 查询逻辑（LEFT JOIN） ==========
    query_map = {
        "微生物": ("GM_name", """
            SELECT mc.GM_name AS source, 
                   m.metabolite_name, 
                   t.gene_symbol, 
                   d.disease_name
            FROM Microbes mc
            LEFT JOIN Microbe_Metabolite mm ON mc.microbe_id = mm.microbe_id
            LEFT JOIN Metabolites m ON mm.metabolite_id = m.metabolite_id
            LEFT JOIN Metabolite_Target mt ON m.metabolite_id = mt.metabolite_id
            LEFT JOIN Targets t ON mt.Gene_id = t.Gene_id
            LEFT JOIN Metabolite_Disease md ON m.metabolite_id = md.metabolite_id
            LEFT JOIN Diseases d ON md.disease_id = d.disease_id
            WHERE {conditions}
        """),
        
        "代谢物": ("metabolite_name", """
            SELECT m.metabolite_name AS source, 
                   t.gene_symbol, 
                   d.disease_name
            FROM Metabolites m
            LEFT JOIN Metabolite_Target mt ON m.metabolite_id = mt.metabolite_id
            LEFT JOIN Targets t ON mt.Gene_id = t.Gene_id
            LEFT JOIN Metabolite_Disease md ON m.metabolite_id = md.metabolite_id
            LEFT JOIN Diseases d ON md.disease_id = d.disease_id
            WHERE {conditions}
        """),
        "靶点": ("gene_symbol", """
            SELECT t.gene_symbol AS source, 
                   m.metabolite_name, 
                   d.disease_name
            FROM Targets t
            LEFT JOIN Metabolite_Target mt ON t.Gene_id = mt.Gene_id
            LEFT JOIN Metabolites m ON mt.metabolite_id = m.metabolite_id
            LEFT JOIN Metabolite_Disease md ON m.metabolite_id = md.metabolite_id
            LEFT JOIN Diseases d ON md.disease_id = d.disease_id
            WHERE {conditions}
        """),
        "病症": ("disease_name", """
            SELECT d.disease_name AS source, 
                   m.metabolite_name, 
                   t.gene_symbol
            FROM Diseases d
            LEFT JOIN Metabolite_Disease md ON d.disease_id = md.disease_id
            LEFT JOIN Metabolites m ON md.metabolite_id = m.metabolite_id
            LEFT JOIN Metabolite_Target mt ON m.metabolite_id = mt.metabolite_id
            LEFT JOIN Targets t ON mt.Gene_id = t.Gene_id
            WHERE {conditions}
        """),
        "食物": ("food_name", """
            SELECT f.food_name AS source, 
                   m.metabolite_name, 
                   t.gene_symbol, 
                   d.disease_name
            FROM FoodSources f
            LEFT JOIN Metabolite_Food mf ON f.food_id = mf.food_id
            LEFT JOIN Metabolites m ON mf.metabolite_id = m.metabolite_id
            LEFT JOIN Metabolite_Target mt ON m.metabolite_id = mt.metabolite_id
            LEFT JOIN Targets t ON mt.Gene_id = t.Gene_id
            LEFT JOIN Metabolite_Disease md ON m.metabolite_id = md.metabolite_id
            LEFT JOIN Diseases d ON md.disease_id = d.disease_id
            WHERE {conditions}
        """),
    }

    key_col, sql_template = query_map[query_type]
    conditions = ' OR '.join([f"LOWER({key_col}) LIKE LOWER(:kw{i})" for i in range(len(keywords))])
    query_str = sql_template.format(conditions=conditions)
    query_sql = text(query_str)
    param_dict = {f'kw{i}': f"%{kw}%" for i, kw in enumerate(keywords)}

    df = pd.read_sql(query_sql, engine, params=param_dict)

    st.markdown("### 🔍 查询结果")
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 下载为 CSV", df.to_csv(index=False), file_name="gutdb_query.csv")

    # ========== 富集分析（同时 GO + KEGG） ==========
    if 'gene_symbol' in df.columns:
        gene_list = df['gene_symbol'].dropna().unique().tolist()
        if gene_list:
            # --- KEGG
            enr_kegg = gp.enrichr(
                gene_list=gene_list,
                gene_sets='KEGG_2021_Human',
                organism='Human',
                outdir=None,
                cutoff=0.1
            )

            # --- GO
            enr_go = gp.enrichr(
                gene_list=gene_list,
                gene_sets='GO_Biological_Process_2021',
                organism='Human',
                outdir=None,
                cutoff=0.1
            )

            # ========== KEGG 处理 ========== 
            if enr_kegg.results is not None and not enr_kegg.results.empty:
                enr_kegg.results['GeneRatio'] = enr_kegg.results['Overlap'].apply(
                    lambda x: int(x.split('/')[0]) / int(x.split('/')[1])
                )
                enr_kegg.results.sort_values("GeneRatio", ascending=False, inplace=True)

                st.markdown("### 🧬 KEGG Pathway Enrichment")
                st.dataframe(enr_kegg.results[['Term', 'Adjusted P-value', 'GeneRatio', 'Genes']], use_container_width=True)
                st.download_button(
                    "📥 下载 KEGG 结果",
                    data=enr_kegg.results.to_csv(index=False),
                    file_name="KEGG_enrichment.csv"
                )

                selected_kegg = st.multiselect(
                    "选择可视化的 KEGG 通路",
                    enr_kegg.results['Term'].tolist(),
                    default=enr_kegg.results['Term'].tolist()[:10]
                )
                enr_kegg_vis = enr_kegg.results[enr_kegg.results['Term'].isin(selected_kegg)]

                c1, c2 = st.columns(2)
                with c1:
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                        plt.figure(figsize=(8, 6))
                        plt.barh(enr_kegg_vis['Term'], enr_kegg_vis['GeneRatio'], color="#4fc3f7")
                        plt.xlabel("Gene Ratio")
                        plt.title("KEGG Barplot")
                        plt.gca().invert_yaxis()
                        plt.tight_layout()
                        plt.savefig(tmpfile.name)
                        with open(tmpfile.name, "rb") as f:
                            bar_data = f.read()
                    # 显示
                    st.markdown(f"<img src='data:image/png;base64,{base64.b64encode(bar_data).decode()}' width='500'/>", unsafe_allow_html=True)
                    # 下载
                    st.download_button(
                        "下载 KEGG Barplot PNG",
                        data=bar_data,
                        file_name="kegg_barplot.png",
                        mime="image/png"
                    )

                with c2:
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                        plt.figure(figsize=(8, 6))
                        plt.scatter(enr_kegg_vis['GeneRatio'], enr_kegg_vis['Term'],
                                    s=enr_kegg_vis['GeneRatio'] * 800,
                                    c=enr_kegg_vis['Adjusted P-value'], cmap='coolwarm', alpha=0.8, edgecolors='k')
                        plt.xlabel("Gene Ratio")
                        plt.title("KEGG Dotplot")
                        plt.gca().invert_yaxis()
                        plt.tight_layout()
                        plt.savefig(tmpfile.name)
                        with open(tmpfile.name, "rb") as f:
                            dot_data = f.read()
                    st.markdown(f"<img src='data:image/png;base64,{base64.b64encode(dot_data).decode()}' width='500'/>", unsafe_allow_html=True)
                    st.download_button(
                        "下载 KEGG Dotplot PNG",
                        data=dot_data,
                        file_name="kegg_dotplot.png",
                        mime="image/png"
                    )

                # KEGG 网络图
                G_kegg = nx.Graph()
                for _, row_kegg in enr_kegg_vis.iterrows():
                    G_kegg.add_node(row_kegg['Term'], color="#81c784", label=row_kegg['Term'])
                    for gene in row_kegg['Genes'].split(";"):
                        G_kegg.add_node(gene, color="#ef5350", label=gene)
                        G_kegg.add_edge(row_kegg['Term'], gene)

                net_kegg = Network(height="500px", width="100%")
                net_kegg.from_nx(G_kegg)
                net_kegg.save_graph("kegg_net.html")

                with open("kegg_net.html", "r", encoding="utf-8") as f:
                    kegg_net_html = f.read()
                st.components.v1.html(kegg_net_html, height=600)
                st.download_button(
                    "下载 KEGG 网络图 HTML",
                    data=kegg_net_html,
                    file_name="kegg_network.html",
                    mime="text/html"
                )


            # ========== GO 处理 ========== 
            if enr_go.results is not None and not enr_go.results.empty:
                enr_go.results['GeneRatio'] = enr_go.results['Overlap'].apply(
                    lambda x: int(x.split('/')[0]) / int(x.split('/')[1])
                )
                enr_go.results.sort_values("GeneRatio", ascending=False, inplace=True)

                st.markdown("### 🧬 GO BP Enrichment")
                st.dataframe(enr_go.results[['Term', 'Adjusted P-value', 'GeneRatio', 'Genes']], use_container_width=True)
                st.download_button(
                    "📥 下载 GO 结果",
                    data=enr_go.results.to_csv(index=False),
                    file_name="GO_enrichment.csv"
                )

                selected_go = st.multiselect(
                    "选择可视化的 GO 条目",
                    enr_go.results['Term'].tolist(),
                    default=enr_go.results['Term'].tolist()[:10]
                )
                enr_go_vis = enr_go.results[enr_go.results['Term'].isin(selected_go)]

                c3, c4 = st.columns(2)
                with c3:
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                        plt.figure(figsize=(8, 6))
                        plt.barh(enr_go_vis['Term'], enr_go_vis['GeneRatio'], color="#f4a261")
                        plt.xlabel("Gene Ratio")
                        plt.title("GO BP Barplot")
                        plt.gca().invert_yaxis()
                        plt.tight_layout()
                        plt.savefig(tmpfile.name)
                        with open(tmpfile.name, "rb") as f:
                            go_bar_data = f.read()
                    st.markdown(f"<img src='data:image/png;base64,{base64.b64encode(go_bar_data).decode()}' width='500'/>", unsafe_allow_html=True)
                    st.download_button(
                        "下载 GO Barplot PNG",
                        data=go_bar_data,
                        file_name="go_barplot.png",
                        mime="image/png"
                    )

                with c4:
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                        plt.figure(figsize=(8, 6))
                        plt.scatter(enr_go_vis['GeneRatio'], enr_go_vis['Term'],
                                    s=enr_go_vis['GeneRatio'] * 800,
                                    c=enr_go_vis['Adjusted P-value'], cmap='coolwarm', alpha=0.8, edgecolors='k')
                        plt.xlabel("Gene Ratio")
                        plt.title("GO BP Dotplot")
                        plt.gca().invert_yaxis()
                        plt.tight_layout()
                        plt.savefig(tmpfile.name)
                        with open(tmpfile.name, "rb") as f:
                            go_dot_data = f.read()
                    st.markdown(f"<img src='data:image/png;base64,{base64.b64encode(go_dot_data).decode()}' width='500'/>", unsafe_allow_html=True)
                    st.download_button(
                        "下载 GO Dotplot PNG",
                        data=go_dot_data,
                        file_name="go_dotplot.png",
                        mime="image/png"
                    )

                # GO 网络图
                G_go = nx.Graph()
                for _, row_go in enr_go_vis.iterrows():
                    G_go.add_node(row_go['Term'], color="#81c784", label=row_go['Term'])
                    for gene in row_go['Genes'].split(";"):
                        G_go.add_node(gene, color="#ef5350", label=gene)
                        G_go.add_edge(row_go['Term'], gene)

                net_go = Network(height="500px", width="100%")
                net_go.from_nx(G_go)
                net_go.save_graph("go_net.html")
                with open("go_net.html", "r", encoding="utf-8") as f:
                    go_net_html = f.read()
                st.components.v1.html(go_net_html, height=600)
                st.download_button(
                    "下载 GO 网络图 HTML",
                    data=go_net_html,
                    file_name="go_network.html",
                    mime="text/html"
                )

    # ========== 原始数据网络图 ==========

    def detect_type(value, row):
        """根据行 row 的多个字段来判断 value 的类型。"""
        if pd.notna(row.get('gene_symbol', None)) and value == row['gene_symbol']:
            return "Target"
        elif pd.notna(row.get('disease_name', None)) and value == row['disease_name']:
            return "Disease"
        elif pd.notna(row.get('metabolite_name', None)) and value == row['metabolite_name']:
            return "Metabolite"
        elif pd.notna(row.get('food_name', None)) and value == row['food_name']:
            return "Food"
        else:
            return "Microbe"

    G_main = nx.Graph()
    for _, row in df.iterrows():
        prev = row['source']
        if prev not in G_main:
            # center node color, or default
            G_main.add_node(prev, label=prev, color=center_colors.get(prev, "#81c784"))
        # from the 2nd column onward
        for col in list(row)[1:]:
            if pd.isna(col):
                continue  # skip None or NaN
            if col not in G_main:
                nodetype = detect_type(col, row)
                G_main.add_node(col, label=col, color=node_colors.get(nodetype, "#ccc"))
            G_main.add_edge(prev, col)
            prev = col

    net_main = Network(height="550px", width="100%", notebook=False)
    net_main.from_nx(G_main)
    net_main.set_options('''
    {
      "nodes": {
        "shape": "dot",
        "size": 20,
        "font": {"size": 16, "color": "#343434"},
        "borderWidth": 2
      },
      "edges": {
        "width": 2,
        "smooth": true,
        "arrows": {
          "to": {"enabled": false},
          "from": {"enabled": false}
        }
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": {"iterations": 150}
      }
    }
    ''')
    net_main.save_graph("graph.html")
    with open("graph.html", "r", encoding="utf-8") as f:
        net_html = f.read()
    st.markdown("### 🌐 查询图谱可视化")
    st.components.v1.html(net_html, height=600)
    st.download_button(
        "下载查询网络图 HTML",
        data=net_html,
        file_name="network_graph.html",
        mime="text/html"
    )

    st.markdown("""
    <div style='font-size:14px; margin-top: 1em;'>
    📌 提示：图中每个颜色对应一个查询关键词，鼠标悬停可查看实体详情。</div>
    <br>
    <div style='font-size:14px;'>
    🎨 <b>节点颜色图例：</b>
    <ul>
      <li style='color:#81c784;'>绿色：查询关键词（中心节点）</li>
      <li style='color:#f4a261;'>橙色：代谢物 Metabolite</li>
      <li style='color:#4fc3f7;'>蓝色：靶点 Target</li>
      <li style='color:#ef5350;'>红色：疾病 Disease</li>
      <li style='color:#90caf9;'>天蓝色：微生物 Microbe</li>
      <li style='color:#ffd54f;'>黄色：食物 Food</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
