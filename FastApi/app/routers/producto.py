from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db
from app.models.producto import Comic
from datetime import datetime
from typing import Optional
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "static/img/comics"

@router.get("/comics")
def listar_comics(db: Session = Depends(get_db)):
    return db.query(Comic).all()

@router.get("/comics/{comic_id}")
def obtener_comic(comic_id: int, db: Session = Depends(get_db)):
    comic = db.query(Comic).get(comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Cómic no encontrado")
    return comic


@router.post("/comics")
def crear_comic(
    nombre: str = Form(...),
    autor: str = Form(...),
    descripcion: str = Form(...),
    categoria: str = Form(...),
    stock: int = Form(...),
    precio: float = Form(...),
    proveedor_id: int = Form(...),
    imagen: UploadFile = File(...),
    editorial: str = Form(...),
    formato: str = Form(...),
    idioma: str = Form(...),
    precio_oferta: float = Form(...),
    costo_proveedor: float = Form(...),
    fecha_lanzamiento: Optional[str] = Form(None)
):
    db: Session = SessionLocal()
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        nombre_archivo = imagen.filename
        ruta_destino = os.path.join(UPLOAD_DIR, nombre_archivo)
        with open(ruta_destino, "wb") as buffer:
            shutil.copyfileobj(imagen.file, buffer)

        fecha = datetime.strptime(fecha_lanzamiento, "%Y-%m-%d").date() if fecha_lanzamiento else None

        nuevo_comic = Comic(
            nombre=nombre,
            autor=autor,
            descripcion=descripcion,
            categoria=categoria,
            stock=stock,
            precio=precio,
            proveedor_id=proveedor_id,
            imagen=nombre_archivo,
            editorial=editorial,
            formato=formato,
            idioma=idioma,
            precio_oferta=precio_oferta,
            costo_proveedor=costo_proveedor,
            fecha_lanzamiento=fecha
        )

        db.add(nuevo_comic)
        db.commit()
        db.refresh(nuevo_comic)

        return {"mensaje": "Cómic creado", "comic": nuevo_comic}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear cómic: {e}")

    finally:
        db.close()

@router.put("/comics/{comic_id}")
def actualizar_comic(
    comic_id: int,
    nombre: str = Form(...),
    autor: str = Form(...),
    descripcion: str = Form(...),
    categoria: str = Form(...),
    stock: int = Form(...),
    precio: float = Form(...),
    proveedor_id: int = Form(...),
    editorial: str = Form(...),
    fecha_lanzamiento: str = Form(...),
    formato: str = Form(...),
    idioma: str = Form(...),
    precio_oferta: float = Form(...),
    costo_proveedor: float = Form(...),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    comic = db.query(Comic).get(comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Cómic no encontrado")

    # Si se sube nueva imagen, reemplazar
    if imagen:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        nombre_archivo = imagen.filename
        ruta_destino = os.path.join(UPLOAD_DIR, nombre_archivo)
        with open(ruta_destino, "wb") as buffer:
            shutil.copyfileobj(imagen.file, buffer)
        comic.imagen = nombre_archivo

    comic.nombre = nombre
    comic.autor = autor
    comic.descripcion = descripcion
    comic.categoria = categoria
    comic.stock = stock
    comic.precio = precio
    comic.proveedor_id = proveedor_id
    comic.editorial = editorial
    comic.fecha_lanzamiento = datetime.strptime(fecha_lanzamiento, "%Y-%m-%d").date() if fecha_lanzamiento else None
    comic.formato = formato
    comic.idioma = idioma
    comic.precio_oferta = precio_oferta
    comic.costo_proveedor = costo_proveedor

    db.commit()
    db.refresh(comic)
    return {"mensaje": "Cómic actualizado", "comic": comic}


@router.delete("/comics/{comic_id}")
def eliminar_comic(comic_id: int, db: Session = Depends(get_db)):
    comic = db.query(Comic).get(comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Cómic no encontrado")

    db.delete(comic)
    db.commit()
    return {"mensaje": "Cómic eliminado correctamente"}
