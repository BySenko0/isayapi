from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from pydantic import BaseModel

class ClienteLogin(BaseModel):
    correo: str
    password: str


class EstadoEnum(str, Enum):
    activo = "activo"
    baja = "baja"

class RolEnum(str, Enum):
    usuario = "usuario"
    admin = "admin"

class ClienteBase(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: str
    membresia: Optional[str] = "Normal"

class ClienteCreate(ClienteBase):
    password: str

class ClienteOut(ClienteBase):
    id_cliente: int
    estado: EstadoEnum
    rol: RolEnum

    class Config:
        orm_mode = True
