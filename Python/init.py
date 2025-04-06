import streamlit as st
from sqlalchemy import create_engine, text

def init_db(x):
    # ========== DATABASE ==========
    engine = create_engine(x)
    st.set_page_config(page_title="GutDB • Microbiome Explorer", layout="wide")

    return engine