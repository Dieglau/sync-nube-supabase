import os
import logging
import requests
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

TN_TOKEN: Optional[str] = os.getenv("TN_TOKEN")
TN_STORE_ID: Optional[str] = os.getenv("TN_STORE_ID")

def is_retryable_error(exception: Any) -> bool:
    """Retries only on 429 or 5xx errors."""
    if isinstance(exception, requests.exceptions.HTTPError):
        status_code = exception.response.status_code if exception.response is not None else 0
        return status_code == 429 or status_code >= 500
    return False

class TiendanubeAPI:
    def __init__(self) -> None:
        if not TN_TOKEN or not TN_STORE_ID:
            raise ValueError("Faltan credenciales de Tiendanube en el archivo .env")
        self.base_url = f"https://api.tiendanube.com/v1/{TN_STORE_ID}"
        self.headers = {
            "Authentication": f"bearer {TN_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "OfertaClick_App (diego@ofertaclick.com)"
        }

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(requests.exceptions.HTTPError)
    )
    def _request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data)
        
        if response.status_code == 429:
            logger.warning("Rate limit alcanzado. Reintentando...")
            response.raise_for_status()
        
        # No raise_for_status aquí para 404, lo manejamos en get_all
        if response.status_code != 404 and not response.ok:
            logger.error(f"Error HTTP {response.status_code}: {response.text}")
            response.raise_for_status()
            
        return response

    def get_all(self, endpoint: str) -> list[Dict[str, Any]]:
        results: list[Dict[str, Any]] = []
        page = 1
        while True:
            logger.info(f"Descargando página {page} de {endpoint}")
            response = self._request("GET", f"{endpoint}?page={page}&per_page=50")
            
            if response.status_code == 404:
                logger.info(f"Fin de paginación alcanzado en página {page}. Total ítems descargados: {len(results)}")
                break
            
            data = response.json()
            if not data:
                break
            results.extend(data)
            page += 1
        return results

    def put(self, endpoint: str, data: Dict[str, Any]) -> Any:
        return self._request("PUT", endpoint, data).json()

    def post(self, endpoint: str, data: Dict[str, Any]) -> Any:
        return self._request("POST", endpoint, data).json()
