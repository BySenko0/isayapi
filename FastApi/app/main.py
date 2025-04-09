from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cliente, proveedor, producto


app = FastAPI(title="API de Mundo Friki")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(cliente.router, prefix="/cliente", tags=["Cliente"])

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de Mundo Friki"}

app.include_router(proveedor.router, tags=["Proveedores"])
app.include_router(producto.router, prefix="/comics", tags=["Cómics"])
