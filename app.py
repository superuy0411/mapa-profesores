import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import base64
import os

st.set_page_config(layout="wide")
st.title("📍 Mapa de Profesores")

# Leer datos desde Excel
df = pd.read_excel("profesores.xlsx")

# Crear dos columnas: izquierda para búsqueda, derecha para mapa
col1, col2 = st.columns([1, 4])

with col1:
    st.subheader("🔎 Búsqueda")
    busqueda = st.text_input("Nombre:", placeholder="Ej: Mastropiero")

# Filtrar según la búsqueda
if busqueda:
    df_filtrado = df[df['nombre_completo'].str.contains(busqueda, case=False, na=False)]
else:
    df_filtrado = df

# Crear mapa
mapa = folium.Map(location=[-17.3895, -66.1568], zoom_start=13)
cluster = MarkerCluster().add_to(mapa)

# Agregar marcadores al mapa
for _, row in df_filtrado.iterrows():
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
                popup_html += f'<br><img src="data:image/jpeg;base64,{encoded}" width="100">'

    folium.Marker(
        location=[row["latitud"], row["longitud"]],
        popup=folium.Popup(popup_html, max_width=250),
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(cluster)

with col2:
    st.subheader("🗺️ Mapa de resultados")
    st_folium(mapa, width=1000, height=600)
