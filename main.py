from itertools import product                
import database_models
from fastapi import Depends, FastAPI 
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

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

@app.get("/product")
def get_all_products(db : Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    return "product not found"

@app.post("/product")
def create_product(product: Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id : int , product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "product updated successfully"
    return "product not found"    

@app.delete("/product")
def delete_product(id : int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "product deleted successfully"       
    return "product not found"  