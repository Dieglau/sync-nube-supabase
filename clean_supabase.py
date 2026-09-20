import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def clean_supabase(sku_to_keep):
    # Obtener todos los productos
    products = supabase.table("productos").select("id, sku_proveedor").execute().data
    
    for p in products:
        sku = p.get('sku_proveedor')
        if sku and sku != sku_to_keep:
            print(f"Eliminando SKU: {sku}")
            supabase.table("productos").delete().eq("id", p['id']).execute()
        else:
            print(f"Manteniendo SKU: {sku}")

if __name__ == "__main__":
    # Usaremos el primero de la lista como prueba
    SKU_PRUEBA = "HUMINIMALISTAB"
    clean_supabase(SKU_PRUEBA)
