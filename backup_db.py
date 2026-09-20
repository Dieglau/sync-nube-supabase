menimport os
import json
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def backup_table(table_name):
    print(f"Iniciando backup de {table_name}...")
    response = supabase.table(table_name).select("*").execute()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{table_name}_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump(response.data, f, indent=4)
    
    print(f"Backup de {table_name} guardado en {filename}")

if __name__ == "__main__":
    backup_table("productos")
    # También respaldamos la nueva tabla de relaciones
    backup_table("combo_relaciones")
