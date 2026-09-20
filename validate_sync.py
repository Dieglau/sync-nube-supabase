import os
from dotenv import load_dotenv
from supabase import create_client
import requests

load_dotenv()

# Configuración
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TN_TOKEN = os.getenv("TN_TOKEN")
TN_STORE_ID = os.getenv("TN_STORE_ID")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
headers = {"Authentication": f"bearer {TN_TOKEN}", "User-Agent": "SyncApp (diego@ofertaclick.com)"}

def get_tn_products():
    response = requests.get(f"https://api.tiendanube.com/v1/{TN_STORE_ID}/products", headers=headers)
    return response.json() if response.status_code == 200 else []

def get_supabase_products():
    # Asumiendo que la tabla se llama 'productos'
    return supabase.table("productos").select("*").execute().data

def validate():
    tn_prods = {p['variants'][0]['sku']: p for p in get_tn_products() if p['variants'][0]['sku']}
    sb_prods = {p['sku']: p for p in get_supabase_products()}

    print(f"Productos en Tiendanube: {len(tn_prods)}")
    print(f"Productos en Supabase: {len(sb_prods)}")

    missing_in_sb = [sku for sku in tn_prods if sku not in sb_prods]
    missing_in_tn = [sku for sku in sb_prods if sku not in tn_prods]

    print(f"SKUs faltantes en Supabase: {len(missing_in_sb)}")
    print(f"SKUs faltantes en Tiendanube: {len(missing_in_tn)}")

if __name__ == "__main__":
    validate()
