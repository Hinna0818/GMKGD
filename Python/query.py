# query.py
from sqlalchemy.sql import text
import pandas as pd
from config import engine

query_map = {
    "微生物": ("GM_name", """
        SELECT mc.GM_name AS source, m.Metabolite_name, t.Gene_symbol, d.Disease_name
        FROM Microbes mc
        LEFT JOIN Microbe_Metabolite mm ON mc.Microbe_id = mm.Microbe_id
        LEFT JOIN Metabolites m ON mm.Metabolite_id = m.Metabolite_id
        LEFT JOIN Metabolite_Target mt ON m.Metabolite_id = mt.Metabolite_id
        LEFT JOIN Targets t ON mt.Gene_id = t.Gene_id
        LEFT JOIN Gene_Disease gd ON t.Gene_id = gd.Gene_id
        LEFT JOIN Diseases d ON gd.Disease_id = d.Disease_id
        WHERE {conditions}
    """),
    "代谢物": ("Metabolite_name", """
            SELECT m.Metabolite_name AS source, 
                   t.Gene_symbol, 
                   d.Disease_name
            FROM Metabolites m
            LEFT JOIN Metabolite_Target mt ON m.Metabolite_id = mt.Metabolite_id
            LEFT JOIN Targets t ON mt.Gene_id = t.Gene_id
            LEFT JOIN Gene_Disease gd ON t.Gene_id = gd.Gene_id
            LEFT JOIN Diseases d ON gd.Disease_id = d.Disease_id
            WHERE {conditions}
        """),
        "靶点": ("Gene_symbol", """
            SELECT t.Gene_symbol AS source, 
                   m.Metabolite_name, 
                   d.Disease_name
            FROM Targets t
            LEFT JOIN Metabolite_Target mt ON t.Gene_id = mt.Gene_id
            LEFT JOIN Metabolites m ON mt.Metabolite_id = m.Metabolite_id
            LEFT JOIN Gene_Disease gd ON t.Gene_id = gd.Gene_id
            LEFT JOIN Diseases d ON gd.Disease_id = d.Disease_id
            WHERE {conditions}
        """),
        "病症": ("Disease_name", """
            SELECT d.Disease_name AS source, 
                   t.Gene_symbol, 
                   m.Metabolite_name
            FROM Diseases d
            LEFT JOIN Gene_Disease gd ON d.Disease_id = gd.Disease_id
            LEFT JOIN Targets t ON gd.Gene_id = t.Gene_id
            LEFT JOIN Metabolite_Target mt ON t.Gene_id = mt.Gene_id
            LEFT JOIN Metabolites m ON mt.Metabolite_id = m.Metabolite_id
            WHERE {conditions}
        """),
        "食物": ("Food_name", """
            SELECT f.Food_name AS source, 
                   m.Metabolite_name, 
                   t.Gene_symbol, 
                   d.Disease_name
            FROM FoodSources f
            LEFT JOIN Metabolite_Food mf ON f.Food_id = mf.Food_id
            LEFT JOIN Metabolites m ON mf.Metabolite_id = m.Metabolite_id
            LEFT JOIN Metabolite_Target mt ON m.Metabolite_id = mt.Metabolite_id
            LEFT JOIN Targets t ON mt.Gene_id = t.Gene_id
            LEFT JOIN Gene_Disease gd ON t.Gene_id = gd.Gene_id
            LEFT JOIN Diseases d ON gd.Disease_id = d.Disease_id
            WHERE {conditions}
        """),
}

def run_query(query_type, keywords):
    key_col, sql_template = query_map[query_type]
    conditions = ' OR '.join([f"LOWER({key_col}) LIKE LOWER(:kw{i})" for i in range(len(keywords))])
    query_str = sql_template.format(conditions=conditions)
    query_sql = text(query_str)
    param_dict = {f'kw{i}': f"%{kw}%" for i, kw in enumerate(keywords)}
    return pd.read_sql(query_sql, engine, params=param_dict)