# backend/routes/licitaciones_routes.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from ..services.licitaciones_service import LicitacionesService
from ..models.licitaciones_model import Licitacion, LicitacionDetalle

router = APIRouter(prefix="/licitaciones", tags=["licitaciones"])

# Configuración - deberías cargar esto desde variables de entorno
API_KEY = "tu_api_key_aqui"
licitaciones_service = LicitacionesService(api_key=API_KEY)

@router.get("/", response_model=List[Licitacion])
async def buscar_licitaciones(
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    estado: Optional[str] = "Publicada",
    region: Optional[int] = None,
    categoria: Optional[str] = None,
    comprador: Optional[str] = None,
    palabra_clave: Optional[str] = None,
    limit: Optional[int] = 100
):
    try:
        licitaciones = licitaciones_service.obtener_licitaciones(
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            estado=estado,
            codigo_region=region,
            codigo_categoria=categoria,
            codigo_comprador=comprador,
            palabra_clave=palabra_clave,
            limit=limit
        )
        return licitaciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{codigo_externo}", response_model=LicitacionDetalle)
async def obtener_detalle_licitacion(codigo_externo: str):
    detalle = licitaciones_service.obtener_detalle_licitacion(codigo_externo)
    if not detalle:
        raise HTTPException(status_code=404, detail="Licitación no encontrada")
    return detalle