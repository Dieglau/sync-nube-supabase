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
headers = {"Authentication": f"bearer {TN_TOKEN}", "User-Agent": "SyncApp (diego@ofertaclick.com)"}

def get_tn_products():
    all_products = []
    page = 1
    while True:
        response = requests.get(f"https://api.tiendanube.com/v1/{TN_STORE_ID}/products?page={page}&per_page=50", headers=headers)
        if response.status_code != 200:
            break
        products = response.json()
        if not products:
            break
        all_products.extend(products)
        page += 1
    return all_products

def sync_nube_to_supabase():
    tn_products = get_tn_products()
    print(f"Total productos en Nube: {len(tn_products)}")
    
    products_to_upsert = []
    for p in tn_products:
        variant = p['variants'][0]
        sku = variant.get('sku')
        if not sku:
            continue
        
        stock_actual = variant.get('stock', 0)
        precio_venta_sugerido = float(variant.get('price', 0))
        visible_en_web = True

        if stock_actual <= 0:
            precio_venta_sugerido = 9999999.00
            visible_en_web = False
            
        data = {
            "sku_proveedor": sku,
            "nombre": p['name']['es'],
            "precio_costo": float(variant.get('cost', 0)),
            "precio_venta_sugerido": precio_venta_sugerido,
            "stock_actual": stock_actual,
            "id_producto_tn": str(p['id']),
            "id_variante_tn": str(variant['id']),
            "visible_en_web": visible_en_web
        }
        products_to_upsert.append(data)
        
        # Realizar upsert en lotes
        if len(products_to_upsert) >= 500:
            supabase.table("productos").upsert(products_to_upsert, on_conflict="sku_proveedor").execute()
            print(f"Sincronizados {len(products_to_upsert)} productos en lote.")
            products_to_upsert = []

    # Upsert final para cualquier producto restante
    if products_to_upsert:
        supabase.table("productos").upsert(products_to_upsert, on_conflict="sku_proveedor").execute()
        print(f"Sincronizados {len(products_to_upsert)} productos restantes en lote final.")
    print("Sincronización de Tiendanube a Supabase completada.")

if __name__ == "__main__":
    sync_nube_to_supabase()
