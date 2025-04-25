# backend/models/licitaciones_model.py

from pydantic import BaseModel
from typing import Optional

class Licitacion(BaseModel):
    CodigoExterno: str
    Nombre: str
    CodigoEstado: int
    Estado: str
    FechaCreacion: str
    FechaCierre: str
    Comprador: dict
    CodigoRegion: Optional[int] = None
    Comuna: Optional[str] = None
    Categoria: Optional[str] = None
    
    class Config:
        extra = "ignore"  # Ignorar campos adicionales que pueda devolver la API

class LicitacionDetalle(Licitacion):
    Descripcion: Optional[str] = None
    Items: Optional[list] = None
    FechasImportantes: Optional[list] = None
    Documentos: Optional[list] = None
    Preguntas: Optional[list] = None