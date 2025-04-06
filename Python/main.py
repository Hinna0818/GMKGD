import streamlit as st
import pandas as pd
import altair as alt
from sqlalchemy import text
from config import engine, generate_center_colors
from dashboard import show_dashboard
from query import run_query
from enrichment import enrich_kegg_and_go
from network_viz import build_network
from sankey_plot import plot_sankey
from init import init_db

## initalize database
engine = init_db("mysql+pymysql://root:he040818@127.0.0.1:3306/gutdb?charset=utf8mb4") ## put your username and code


# ========== 路由切换 ==========
if "show_query" not in st.session_state:
    st.session_state.show_query = False

if st.session_state.show_query:
    if st.button("🔙 返回首页"):
        st.session_state.show_query = False

# ✅ 展示首页
if not st.session_state.show_query:
    show_dashboard()
    st.stop()   

# ========== 查询设置 ==========
st.sidebar.header("🔎 查询设置")
query_type = st.sidebar.selectbox("请选择查询类型 (Select Query Type)", ["微生物", "代谢物", "靶点", "病症", "食物"])


@st.cache_data
def get_keywords_by_type(qtype):
    table_map = {
        "微生物": ("Microbes", "GM_name"),
        "代谢物": ("Metabolites", "Metabolite_name"),
        "靶点": ("Targets", "Gene_symbol"),
        "病症": ("Diseases", "Disease_name"),
        "食物": ("FoodSources", "Food_name"),
    }
    table, column = table_map[qtype]
    with engine.connect() as conn:
        sql = text(f"SELECT DISTINCT {column} FROM {table} ORDER BY {column}")
        return [row[0] for row in conn.execute(sql)]


all_keywords = get_keywords_by_type(query_type)
keyword_input = st.sidebar.text_input("输入关键词 (可模糊匹配)", "")
suggested_keywords = [k for k in all_keywords if keyword_input.lower() in k.lower()]
keywords = st.sidebar.multiselect("关键词（支持多选）", options=suggested_keywords if keyword_input else all_keywords)
search_btn = st.sidebar.button("🚀 开始查询")


# ========== main ==========
if search_btn and keywords:
    center_colors = generate_center_colors(keywords)    
    df = run_query(query_type, keywords)
    st.markdown("### 🔍 查询结果")
    st.dataframe(df, use_container_width=True)
    st.download_button("📅 下载CSV", df.to_csv(index=False), file_name="gutdb_query.csv")

    # Sankey plot
    plot_sankey(df)

    # KEGG and GO enrichment analysis and visualization
    enrich_kegg_and_go(df)

    # Network
    build_network(df, center_colors)
