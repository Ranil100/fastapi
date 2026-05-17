from itertools import product                
import database_models
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI 
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session


database_models.base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "welcome to the show"

products = [
    Product(id=1, name="phone", description="budget phone", price=100.0, quantity=10),
    Product(id=2, name="Laptop", description="gaming laptop", price=700.0, quantity=10),
    Product(id=5, name="pen", description="ink pen", price=50.0, quantity=10),
    Product(id=6, name="desk", description="decor table", price=400.0, quantity=10)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()    

def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    
    if count == 0:
     for product in products:
        db.add(database_models.Product(**product.model_dump()))

    db.commit()

init_db() 

@app.get("/products")
def get_all_products(db : Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "product not found"

@app.post("/products")
def create_product(product: Product , db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products")
def update_product(id : int , product: Product , db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product :
        db_product.name = Product.name
        db_product.description = Product.description
        db_product.price = Product.price
        db_product.quantity = Product.quantity
        db.commit()
        return "product updated"
    else:
        return "product not found"

@app.delete("/products")
def delete_product(id : int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
       db.delete(db_product)
       db.commit()
       return "product deleted"
    else:
       return "product not found"  