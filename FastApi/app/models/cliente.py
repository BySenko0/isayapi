from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

class EstadoEnum(str, enum.Enum):
    activo = "activo"
    baja = "baja"

class RolEnum(str, enum.Enum):
    usuario = "usuario"
    admin = "admin"

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    correo = Column(String(100), unique=True, index=True)
    telefono = Column(String(15))
    membresia = Column(String(20))
    password = Column(String(255))
    estado = Column(Enum(EstadoEnum), default="activo")
    rol = Column(Enum(RolEnum), default="usuario")
