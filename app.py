import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from PIL import Image
import base64
import os

st.set_page_config(layout="wide")
st.title("Mapa de Profesores")

# Leer datos desde Excel
df = pd.read_excel("profesores.xlsx")

# Crear mapa centrado en Cochabamba
mapa = folium.Map(location=[-17.3895, -66.1568], zoom_start=13)
cluster = MarkerCluster().add_to(mapa)

# Cargar marcadores
for _, row in df.iterrows():
    popup_html = f"""
    <b>{row['nombre_completo']}</b><br>
    📍 {row['direccion']}<br>
    📞 {row['telefono']}<br>
    """
    if pd.notna(row['foto']):
        img_path = f"fotos/{row['foto']}"
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                img_tag = f'<img src="data:image/jpeg;base64,{encoded}" width="100">'
                popup_html += img_tag

    folium.Marker(
        location=[row["latitud"], row["longitud"]],
        popup=folium.Popup(popup_html, max_width=250),
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(cluster)

st_folium(mapa, width=1000, height=600)

        r["direccion"] = direccion_edit
        if foto_edit:
            r["foto"] = base64.b64encode(foto_edit.read()).decode()
        st.success("Registro actualizado.")
        st.session_state.edit_index = None
