
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date


class Comic(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    categoria = Column(String(50))
    stock = Column(Integer)
    precio = Column(Float)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id_proveedor"))
    imagen = Column(String(255))
    autor = Column(String(100))
    descripcion = Column(String(500))
    editorial = Column(String(100))
    fecha_lanzamiento = Column(Date)
    formato = Column(String(50))
    idioma = Column(String(50))
    precio_oferta = Column(Float)
    costo_proveedor = Column(Float)
    # Relación con proveedor (opcional si necesitas acceder al proveedor desde el cómic)
    proveedor = relationship("Proveedor", back_populates="comics")
