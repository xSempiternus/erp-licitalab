# backend/services/licitaciones_service.py

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from ..models.licitaciones_model import Licitacion

class LicitacionesService:
    def __init__(self, api_key: str):
        self.base_url = "https://api.mercadopublico.cl"
        self.api_key = api_key
    
    def obtener_licitaciones(
        self,
        fecha_desde: str = None,
        fecha_hasta: str = None,
        estado: str = "Publicada",
        codigo_region: str = None,
        codigo_categoria: str = None,
        codigo_comprador: str = None,
        palabra_clave: str = None,
        limit: int = 100
    ) -> List[Licitacion]:
        """
        Obtiene licitaciones según los parámetros de búsqueda
        """
        endpoint = f"{self.base_url}/servicios/v1/publico/licitaciones.json"
        
        # Si no se especifican fechas, usar última semana
        if not fecha_desde or not fecha_hasta:
            fecha_hasta = datetime.now().strftime("%Y-%m-%d")
            fecha_desde = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        params = {
            "fechaDesde": fecha_desde,
            "fechaHasta": fecha_hasta,
            "estado": estado,
            "ticket": self.api_key
        }
        
        # Filtros opcionales
        if codigo_region:
            params["codigoRegion"] = codigo_region
        if codigo_categoria:
            params["codigoCategoria"] = codigo_categoria
        if codigo_comprador:
            params["codigoComprador"] = codigo_comprador
        if palabra_clave:
            params["palabraClave"] = palabra_clave
        
        response = requests.get(endpoint, params=params)
        
        if response.status_code == 200:
            data = response.json()
            licitaciones = [Licitacion(**item) for item in data.get("Listado", [])[:limit]]
            return licitaciones
        else:
            raise Exception(f"Error al obtener licitaciones: {response.status_code}")
    
    def obtener_detalle_licitacion(self, codigo_externo: str) -> Optional[Dict]:
        """
        Obtiene el detalle completo de una licitación específica
        """
        endpoint = f"{self.base_url}/servicios/v1/publico/licitaciones/{codigo_externo}.json"
        params = {"ticket": self.api_key}
        
        response = requests.get(endpoint, params=params)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            raise Exception(f"Error al obtener detalle: {response.status_code}")