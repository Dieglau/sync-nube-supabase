import streamlit as st
import pandas as pd
from sync_engine import get_db_products, sync_nube_to_db
import logging

st.set_page_config(layout="wide")
st.title("Gestión de Productos - OfertaClick")

if st.button("Sincronizar Stock desde Nube"):
    with st.spinner("Sincronizando..."):
        sync_nube_to_db()
        st.success("Sincronización completada")

# Cargar datos
db_products = get_db_products()
df = pd.DataFrame(list(db_products.values()))

# Filtros
st.sidebar.header("Filtros")
sku_filter = st.sidebar.text_input("Filtrar por SKU")
if sku_filter:
    df = df[df['sku_proveedor'].str.contains(sku_filter, case=False)]

st.dataframe(df)

# Acciones masivas
st.header("Acciones Masivas")
uploaded_file = st.file_uploader("Subir Excel de cambios", type=["xlsx"])
if uploaded_file:
    df_upload = pd.read_excel(uploaded_file)
    st.write("Vista previa:", df_upload.head())
    if st.button("Aplicar cambios"):
        st.warning("Lógica de aplicación de cambios pendiente de implementar")
