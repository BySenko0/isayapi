from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import proveedor as models
from app.schemas import proveedor as schemas
from datetime import date

router = APIRouter()

@router.get("/proveedores", response_model=list[schemas.ProveedorOut])
def listar_proveedores(db: Session = Depends(get_db)):
    return db.query(models.Proveedor).all()

@router.get("/proveedores/{proveedor_id}", response_model=schemas.ProveedorOut)
def obtener_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    proveedor = db.query(models.Proveedor).get(proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

@router.post("/proveedores", response_model=schemas.ProveedorOut)
def crear_proveedor(data: schemas.ProveedorCreate, db: Session = Depends(get_db)):
    nuevo = models.Proveedor(**data.dict(), ultima_fecha_modificacion=date.today())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/proveedores/{proveedor_id}", response_model=schemas.ProveedorOut)
def actualizar_proveedor(proveedor_id: int, data: schemas.ProveedorUpdate, db: Session = Depends(get_db)):
    proveedor = db.query(models.Proveedor).get(proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(proveedor, attr, value)
    proveedor.ultima_fecha_modificacion = date.today()
    db.commit()
    db.refresh(proveedor)
    return proveedor

@router.delete("/proveedores/{proveedor_id}")
def eliminar_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    proveedor = db.query(models.Proveedor).get(proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    db.delete(proveedor)
    db.commit()
    return {"ok": True}
