import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def plot_sankey(df):
    if not all(col in df.columns for col in ['source', 'Metabolite_name', 'Gene_symbol']):
        st.warning("缺少必要列，无法绘制桑基图。")
        return

    links = []
    label_set = set()
    entity_type_map = {}  # 记录每个 label 是哪种实体类型

    for _, row in df.iterrows():
        src = row.get("source")
        mid = row.get("Metabolite_name")
        tgt = row.get("Gene_symbol")

        if pd.isna(src) or pd.isna(mid) or pd.isna(tgt):
            continue

        label_set.update([src, mid, tgt])
        entity_type_map[src] = "Microbe"
        entity_type_map[mid] = "Metabolite"
        entity_type_map[tgt] = "Target"

        links.append((src, mid))
        links.append((mid, tgt))

    label_list = list(label_set)
    label_index = {label: i for i, label in enumerate(label_list)}

    # 定义不同类型节点的颜色
    color_map = {
        "Microbe": "#90caf9",
        "Metabolite": "#f4a261",
        "Target": "#4fc3f7"
    }
    node_colors = [color_map.get(entity_type_map.get(label, ""), "#cccccc") for label in label_list]

    sankey_data = {
        "source": [label_index[src] for src, tgt in links],
        "target": [label_index[tgt] for src, tgt in links],
        "value": [1] * len(links)
    }

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=25,
            thickness=30,
            line=dict(color="black", width=0.5),
            label=label_list,
            color=node_colors,
        ),
        link=dict(
            source=sankey_data["source"],
            target=sankey_data["target"],
            value=sankey_data["value"],
            color="rgba(150,150,150,0.4)"  # 较浅透明灰色线条
        )
    )])

    fig.update_layout(
        title_text="🔄 微生物 → 代谢物 → 靶点 Sankey Diagram",
        font=dict(size=14, color='black'),
        width=1400,
        height=600,
        margin=dict(l=40, r=40, t=60, b=30)
    )

    st.markdown("### 🔄 微生物-代谢物-靶点 Sankey 图")
    st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "📥 下载 Sankey JSON",
        data=fig.to_json(),
        file_name="sankey_microbe_metabolite_target.json"
    )
