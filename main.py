from fastapi import FastAPI
from routes import products, orders
from db import connect_to_mongo

app = FastAPI(
    title="HROne Backend",
    description="Backend service",
    version="1.0.0"
)

# Connect to MongoDB on startup
@app.on_event("startup")
def startup_db():
    connect_to_mongo()
    print("Connected to MongoDB and indexes are ready.")

# Root health check
@app.get("/", tags=["Health"])
def root():
    return {"message": "HROne Backend is running!"}

# Register routes
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

