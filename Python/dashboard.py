import streamlit as st
import pandas as pd
import altair as alt
from sqlalchemy import text
from config import engine 

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
    col1.metric("🧬 Microbes", count_table("Microbes"))
    col2.metric("🧪 Metabolites", count_table("Metabolites"))
    col3.metric("🎯 Targets", count_table("Targets"))
    col4.metric("🩺 Diseases", count_table("Diseases"))
    col5.metric("🍎 Foods", count_table("FoodSources"))

    # === 微生物等级分布图 ===
    with engine.connect() as conn:
        micro_df = pd.read_sql("SELECT GM_Rank, COUNT(*) AS count FROM Microbes GROUP BY GM_Rank", conn)

    if not micro_df.empty:
        st.markdown("""
        <h4 style='color:#388e3c; margin-top:2rem;'>🧬 Microbe Rank Distribution</h4>
        """, unsafe_allow_html=True)
        rank_keyword = st.text_input("模糊搜索微生物等级", "")
        min_micro_count = st.slider("数量阈值", 1, int(micro_df['count'].max()), 1)
        filtered_micro = micro_df[micro_df['count'] >= min_micro_count]
        if rank_keyword:
            filtered_micro = filtered_micro[filtered_micro['GM_Rank'].str.contains(rank_keyword, case=False)]

        chart = alt.Chart(filtered_micro).mark_bar(size=18, color='#4fc3f7').encode(
            y=alt.Y('GM_Rank:N', sort='-x', title='Rank'),
            x=alt.X('count:Q', title='数量'),
            tooltip=['GM_Rank', 'count']
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)

    # === 数据库说明 ===
    st.markdown("""
    <hr style='margin-top:2rem; margin-bottom:1rem;'>
    <h4 style='color:#388e3c;'>📘 数据库说明</h4>
    <ul style='font-size:15px;'>
        <li>覆盖微生物、代谢物、靶点、病症和食物五大模块。</li>
        <li>支持多实体关键词模糊查询和图谱可视化。</li>
        <li>内嵌 KEGG 与 GO_BP 富集分析，全面解读代谢物靶点。</li>
        <li>查询与分析结果支持下载。</li>
    </ul>
    """, unsafe_allow_html=True)

    if st.button("🚀 前往图谱查询", type="primary"):
        st.session_state.show_query = True
