from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteOut, ClienteLogin  
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependencia de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login_cliente(data: ClienteLogin, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.correo == data.correo).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Correo no encontrado")

    if not pwd_context.verify(data.password, cliente.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {
        "mensaje": "Inicio de sesión exitoso",
        "cliente_id": cliente.id_cliente,
        "nombre": cliente.nombre,
        "correo": cliente.correo,
        "rol": cliente.rol
    }


@router.post("/", response_model=ClienteOut)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(cliente.password)

    hashed_password = pwd_context.hash(cliente.password)
    nuevo_cliente = Cliente(
        nombre=cliente.nombre,
        correo=cliente.correo,
        telefono=cliente.telefono,
        membresia=cliente.membresia,
        password=hashed_password,
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

@router.get("/", response_model=list[ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()
