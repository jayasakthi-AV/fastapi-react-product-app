from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI()

# ---------------- DATABASE SETUP ----------------

DATABASE_URL = "sqlite:///./products.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- TABLE MODEL ----------------

class ProductTable(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)

# Create table
Base.metadata.create_all(bind=engine)

# ---------------- PYDANTIC MODEL ----------------

class Product(BaseModel):
    id: int
    name: str
    price: float

# ---------------- DATABASE SESSION ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- GET ALL PRODUCTS ----------------

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(ProductTable).all()
    return products

# ---------------- GET PRODUCT BY ID ----------------

@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductTable).filter(ProductTable.id == product_id).first()

    if product:
        return product
    return {"message": "Product not found"}

# ---------------- ADD PRODUCT ----------------

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    new_product = ProductTable(
        id=product.id,
        name=product.name,
        price=product.price
    )

    db.add(new_product)
    db.commit()

    return {"message": "Product added"}

# ---------------- UPDATE PRODUCT ----------------

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product, db: Session = Depends(get_db)):

    product = db.query(ProductTable).filter(ProductTable.id == product_id).first()

    if product:
        product.name = updated_product.name
        product.price = updated_product.price

        db.commit()

        return {"message": "Product updated"}

    return {"message": "Product not found"}

# ---------------- DELETE PRODUCT ----------------

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(ProductTable).filter(ProductTable.id == product_id).first()

    if product:
        db.delete(product)
        db.commit()

        return {"message": "Product deleted"}

    return {"message": "Product not found"}