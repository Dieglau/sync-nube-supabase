import os
import logging
from decimal import Decimal
from typing import Dict, Any, List
from dotenv import load_dotenv
from supabase import create_client, Client
from api_tiendanube import TiendanubeAPI

load_dotenv()
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
tn_api = TiendanubeAPI()

def get_db_products() -> Dict[str, Any]:
    response = supabase.table("productos").select("*").execute()
    return {str(p["sku_proveedor"]): p for p in response.data}

def get_combos() -> List[Dict[str, Any]]:
    response = supabase.table("combos").select("*").execute()
    return response.data

def update_combo_stock(combo_sku: str, db_products: Dict[str, Any]):
    # Obtener componentes del combo
    components = supabase.table("combos").select("*").eq("combo_sku", combo_sku).execute().data
    
    # Calcular stock mínimo basado en componentes
    min_stock = float('inf')
    for comp in components:
        comp_sku = comp['componente_sku']
        qty = comp['cantidad']
        comp_stock = db_products.get(comp_sku, {}).get('stock_actual', 0)
        min_stock = min(min_stock, comp_stock // qty)
    
    # Actualizar stock del combo
    supabase.table("productos").update({"stock_actual": int(min_stock)}).eq("sku_proveedor", combo_sku).execute()
    logger.info(f"Combo {combo_sku} actualizado a stock {min_stock}")

def sync_nube_to_db():
    db_products = get_db_products()
    tn_variants = tn_api.get_all("variants")
    
    for variant in tn_variants:
        sku = variant.get("sku")
        if not sku or sku not in db_products:
            continue
            
        stock_nube = int(variant.get("stock", 0) or 0)
        db_prod = db_products[sku]
        
        if db_prod.get("stock_actual") != stock_nube:
            supabase.table("productos").update({"stock_actual": stock_nube}).eq("sku_proveedor", sku).execute()
            db_products[sku]["stock_actual"] = stock_nube
            logger.info(f"SKU {sku} actualizado: Stock {stock_nube}")
            
            # Si es un componente, actualizar combos relacionados
            combos = supabase.table("combos").select("combo_sku").eq("componente_sku", sku).execute().data
            for combo in combos:
                update_combo_stock(combo['combo_sku'], db_products)
