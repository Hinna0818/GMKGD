from sqlalchemy import create_engine
import random

# MySQL connection
engine = create_engine("mysql+pymysql://root:he040818@127.0.0.1:3306/gutdb?charset=utf8mb4")

# Color palette for network
color_palette = ["#81c784", "#aed581", "#ffd54f", "#ffb74d", "#4fc3f7", "#9575cd", "#e57373"]
node_colors = {
    "Microbe": "#90caf9", "Metabolite": "#f4a261", "Target": "#4fc3f7",
    "Disease": "#ef5350", "Food": "#ffd54f"
}

def generate_center_colors(keywords):
    return {kw: random.choice(color_palette) for kw in keywords}
