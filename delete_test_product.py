import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def delete_test_product(sku):
    # Eliminar de Supabase
    response = supabase.table("productos").delete().eq("sku_proveedor", sku).execute()
    print(f"Producto de prueba {sku} eliminado de Supabase.")

if __name__ == "__main__":
    delete_test_product("TEST-COMBO-001")
