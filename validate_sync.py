import os
from dotenv import load_dotenv
from supabase import create_client
import requests
from api_tiendanube import TiendanubeAPI

load_dotenv()

# Configuración
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TN_TOKEN = os.getenv("TN_TOKEN")
TN_STORE_ID = os.getenv("TN_STORE_ID")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# Se inicializa la API de Tiendanube para usar su método get_all con paginación mejorada
tn_api = TiendanubeAPI()

def get_tn_products():
    # Usar el método get_all de TiendanubeAPI para obtener todos los productos con paginación robusta
    return tn_api.get_all("products")

def get_supabase_products():
    # Asumiendo que la tabla se llama 'productos'
    return supabase.table("productos").select("*").execute().data

def validate():
    tn_prods = {p['variants'][0]['sku']: p for p in get_tn_products() if p['variants'][0]['sku']}
    sb_prods = {p['sku_proveedor']: p for p in get_supabase_products() if p.get('sku_proveedor')}

    print(f"Productos en Tiendanube: {len(tn_prods)}")
    print(f"Productos en Supabase: {len(sb_prods)}")

    missing_in_sb = [sku for sku in tn_prods if sku not in sb_prods]
    missing_in_tn = [sku for sku in sb_prods if sku not in tn_prods]

    print(f"SKUs faltantes en Supabase: {len(missing_in_sb)}")
    print(f"SKUs faltantes en Tiendanube: {len(missing_in_tn)}")
    print("--- SKUs en Supabase pero no en Tiendanube (Candidatos a limpieza): ---")
    for sku in missing_in_tn[:10]: # Mostrar primeros 10
        print(sku)

if __name__ == "__main__":
    validate()
