from fastapi import APIRouter, HTTPException, Query
from db import get_db
from models import ProductModel
from bson import ObjectId
from typing import Optional

router = APIRouter()

# Create a new product (returns "id")
@router.post("/", status_code=201)
def create_product(product: ProductModel):
    db = get_db()

    #  Validation: product must have at least one size
    if not product.sizes or len(product.sizes) == 0:
        raise HTTPException(status_code=400, detail="At least one size is required.")

    #  Validation: each size entry must be valid
    for size in product.sizes:
        if not size.size or size.quantity < 0:
            raise HTTPException(status_code=400, detail="Each size must have a valid name and non-negative quantity.")

    #  Validation: price must be non-negative
    if product.price < 0:
        raise HTTPException(status_code=400, detail="Price must be a non-negative value.")

    result = db.products.insert_one(product.dict())
    return {"id": str(result.inserted_id)}  # Use "id" instead of "_id"


#  Get list of products with search, filter, pagination
@router.get("/", status_code=200)
def list_products(
    name: Optional[str] = Query(None, min_length=1, max_length=100),
    size: Optional[str] = Query(None, min_length=1, max_length=10),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    db = get_db()
    query = {}

    #  Case-insensitive name search using regex
    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    #  Filter by nested "size" inside "sizes" array
    if size:
        query["sizes"] = {"$elemMatch": {"size": size}}

    #  Get filtered, paginated products sorted by _id
    cursor = db.products.find(query).skip(offset).limit(limit).sort("_id")

    #  Format response
    products = [
        {
            "id": str(doc["_id"]),
            "name": doc.get("name", ""),
            "price": doc.get("price", 0.0),
            "sizes": doc.get("sizes", [])
        }
        for doc in cursor
    ]

    return {
        "data": products,
        "page": {
            "next": offset + limit,
            "limit": limit,
            "previous": max(offset - limit, 0)
        }
    }








