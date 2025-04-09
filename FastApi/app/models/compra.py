from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Compra(Base):
    __tablename__ = "compras"  # Nombre de la tabla en la base de datos

    id_compra = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id_cliente"))  # Relación con Cliente
    fecha_compra = Column(DateTime, default=datetime.now())
    total = Column(Float)
    estado = Column(String(20), default="completada")  # ej: "pendiente", "cancelada"

    # Relación opcional para acceder a los items de la compra
    items = relationship("ItemCompra", back_populates="compra")

class ItemCompra(Base):
    __tablename__ = "items_compra"

    id_item = Column(Integer, primary_key=True, index=True)
    compra_id = Column(Integer, ForeignKey("compras.id_compra"))  # Relación con Compra
    producto_id = Column(Integer, ForeignKey("productos.id_producto"))  # Relación con Comic/Producto
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    subtotal = Column(Float)

    # Relaciones
    compra = relationship("Compra", back_populates="items")
    producto = relationship("Comic")  # Relación con el modelo Comic (producto)