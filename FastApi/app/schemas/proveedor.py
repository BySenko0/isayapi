from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProveedorBase(BaseModel):
    nombre: str
    correo: str
    telefono: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(ProveedorBase):
    ultima_fecha_modificacion: Optional[date] = None

class ProveedorOut(ProveedorBase):
    id_proveedor: int
    ultima_fecha_modificacion: Optional[date]

    class Config:
        orm_mode = True
