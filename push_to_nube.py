import os
from dotenv import load_dotenv
from supabase import create_client
import requests

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TN_TOKEN = os.getenv("TN_TOKEN")
TN_STORE_ID = os.getenv("TN_STORE_ID")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
headers = {
    "Authentication": f"bearer {TN_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "SyncApp (diego@ofertaclick.com)"
}

def push_product_to_nube(sku):
    # Obtener producto de Supabase
    product = supabase.table("productos").select("*").eq("sku_proveedor", sku).execute().data
    if not product:
        print(f"Producto {sku} no encontrado en Supabase")
        return
    
    p = product[0]
    
    # Preparar payload para Tiendanube
    payload = {
        "name": {"es": p['nombre']},
        "variants": [{
            "sku": p['sku_proveedor'],
            "price": str(p['precio_venta_sugerido']),
            "cost": str(p['precio_costo']),
            "stock": p['stock_actual']
        }]
    }
    
    # Enviar a Tiendanube
    response = requests.post(f"https://api.tiendanube.com/v1/{TN_STORE_ID}/products", json=payload, headers=headers)
    
    if response.status_code in [200, 201]:
        print(f"Producto {sku} enviado exitosamente a Tiendanube")
        # Actualizar IDs en Supabase si es necesario
        new_prod = response.json()
        supabase.table("productos").update({
            "id_producto_tn": str(new_prod['id']),
            "id_variante_tn": str(new_prod['variants'][0]['id'])
        }).eq("sku_proveedor", sku).execute()
    else:
        print(f"Error al enviar {sku}: {response.text}")

if __name__ == "__main__":
    push_product_to_nube("TEST-COMBO-001")
