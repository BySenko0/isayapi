from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Proveedor(Base):
    __tablename__ = "proveedores"

    id_proveedor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    correo = Column(String(100))
    telefono = Column(String(20))
    ultima_fecha_abastecimiento = Column(Date, nullable=True)
    ultima_fecha_modificacion = Column(Date, nullable=True)

    # Relación con productos
    comics = relationship("Comic", back_populates="proveedor")
