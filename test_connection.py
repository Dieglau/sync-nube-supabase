import os
from dotenv import load_dotenv
from supabase import create_client
import requests

load_dotenv()

# Test Supabase
try:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase = create_client(url, key)
    print("Supabase: Conexión exitosa.")
except Exception as e:
    print(f"Supabase: Error - {e}")

# Test Tiendanube
try:
    token = os.getenv("TN_TOKEN")
    store_id = os.getenv("TN_STORE_ID")
    headers = {"Authentication": f"bearer {token}", "User-Agent": "SyncApp (diego@ofertaclick.com)"}
    response = requests.get(f"https://api.tiendanube.com/v1/{store_id}/products", headers=headers)
    if response.status_code == 200:
        print("Tiendanube: Conexión exitosa.")
    else:
        print(f"Tiendanube: Error {response.status_code} - {response.text}")
except Exception as e:
    print(f"Tiendanube: Error - {e}")
