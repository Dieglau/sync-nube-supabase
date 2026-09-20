import time
import logging
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def keep_alive():
    while True:
        try:
            # Consulta simple para mantener la conexión activa
            supabase.table("productos").select("sku_proveedor").limit(1).execute()
            logger.info("Ping a Supabase exitoso.")
        except Exception as e:
            logger.error(f"Error en ping: {e}")
        
        # Esperar 10 minutos (600 segundos)
        time.sleep(600)

if __name__ == "__main__":
    logger.info("Iniciando proceso de keep-alive para Supabase...")
    keep_alive()
