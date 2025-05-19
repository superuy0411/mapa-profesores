import streamlit as st
from streamlit_folium import st_folium
import folium
import base64
import json
import os

# Cargar datos existentes (o iniciar vacío)
if os.path.exists("data.json"):
    with open("data.json", "r", encoding="utf-8") as f:
        registros = json.load(f)
else:
    registros = []

nuevo_registro = {
    "nombre": nombre,
    "telefono": telefono,
    "direccion": direccion,
    "lat": lat,
    "lon": lon
}
registros.append(nuevo_registro)

# Guardar los cambios
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(registros, f, ensure_ascii=False, indent=4)


st.set_page_config(layout="wide")
st.title("📍 Registro de Profesores")

# Inicializar sesión
if "registros" not in st.session_state:
    st.session_state.registros = []

if "map_center" not in st.session_state:
    st.session_state.map_center = [-17.3895, -66.1568]  # Centro de Cocha

if "click_coords" not in st.session_state:
    st.session_state.click_coords = None

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# Crear mapa base
m = folium.Map(location=st.session_state.map_center, zoom_start=15)

# Agregar los marcadores existentes
for i, r in enumerate(st.session_state.registros):
    popup = f"<b>{r['nombre']}</b><br>📞 {r['telefono']}<br>📍 {r['direccion']}"
    if r['foto']:
        popup += f"<br><img src='data:image/jpeg;base64,{r['foto']}' width='100'>"
    folium.Marker(
        location=[r["lat"], r["lon"]],
        popup=popup,
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(m)

# Mostrar mapa interactivo
map_data = st_folium(m, height=600, width=1000)

# Capturar clic para registrar nueva ubicación
if map_data and map_data.get("last_clicked"):
    coords = map_data["last_clicked"]
    st.session_state.click_coords = coords

# LADO IZQUIERDO - Lista de profesores y edición
with st.sidebar:
    st.header("👩‍🏫 Profesores Registrados")
    if not st.session_state.registros:
        st.info("No hay profesores registrados.")
    else:
        for idx, r in enumerate(st.session_state.registros):
            with st.expander(f"{r['nombre']}"):
                st.markdown(f"📞 {r['telefono']}")
                st.markdown(f"📍 {r['direccion']}")
                if r["foto"]:
                    st.image(base64.b64decode(r["foto"]), width=150)
                if st.button("✏️ Editar", key=f"editar_{idx}"):
                    st.session_state.edit_index = idx

# Registrar nuevo profesor (si se hizo clic en el mapa)
if st.session_state.click_coords and st.session_state.edit_index is None:
    st.subheader("➕ Registrar nuevo profesor")
    nombre = st.text_input("Nombre completo")
    telefono = st.text_input("Teléfono")
    direccion = st.text_input("Dirección")
    foto = st.file_uploader("Foto del profesor", type=["jpg", "jpeg", "png"])
    if st.button("Guardar"):
        foto_data = None
        if foto:
            foto_data = base64.b64encode(foto.read()).decode()

        st.session_state.registros.append({
            "nombre": nombre,
            "telefono": telefono,
            "direccion": direccion,
            "lat": st.session_state.click_coords["lat"],
            "lon": st.session_state.click_coords["lng"],
            "foto": foto_data
        })
        st.success("Profesor registrado.")
        st.session_state.click_coords = None

# Editar profesor
if st.session_state.edit_index is not None:
    st.subheader("✏️ Editar profesor")
    r = st.session_state.registros[st.session_state.edit_index]
    nombre_edit = st.text_input("Nombre completo", value=r["nombre"])
    telefono_edit = st.text_input("Teléfono", value=r["telefono"])
    direccion_edit = st.text_input("Dirección", value=r["direccion"])
    foto_edit = st.file_uploader("Nueva foto (opcional)", type=["jpg", "jpeg", "png"])

    if st.button("Actualizar"):
        r["nombre"] = nombre_edit
        r["telefono"] = telefono_edit
        r["direccion"] = direccion_edit
        if foto_edit:
            r["foto"] = base64.b64encode(foto_edit.read()).decode()
        st.success("Registro actualizado.")
        st.session_state.edit_index = None
