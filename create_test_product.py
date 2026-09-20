import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_test_product():
    # SKU que no existe en Tiendanube para probar el push
    test_sku = "TEST-COMBO-001"
    data = {
        "sku_proveedor": test_sku,
        "nombre": "Producto de Prueba para Push",
        "precio_costo": 100.0,
        "precio_venta_sugerido": 200.0,
        "stock_actual": 10
    }
    
    # Insertar en Supabase
    response = supabase.table("productos").insert(data).execute()
    print(f"Producto de prueba creado: {test_sku}")
    return test_sku

if __name__ == "__main__":
    create_test_product()
