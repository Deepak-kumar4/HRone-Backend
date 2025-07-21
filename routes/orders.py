from fastapi import APIRouter, HTTPException
from db import get_db
from models import OrderModel
from bson import ObjectId

router = APIRouter()

# Create a new order with validation and calculated total
@router.post("/", status_code=201)
def create_order(order: OrderModel):
    db = get_db()

    if not order.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item.")

    # Step 1: Validate ObjectIds and quantities
    product_ids = []
    for item in order.items:
        if not ObjectId.is_valid(item.product_id):
            raise HTTPException(status_code=400, detail=f"Invalid product ID: {item.product_id}")
        if item.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than 0.")
        product_ids.append(ObjectId(item.product_id))

    # Step 2: Fetch all products in one go
    products = db.products.find({"_id": {"$in": product_ids}})
    product_map = {str(p["_id"]): p for p in products}

    # Step 3: Calculate total price
    total_price = 0
    for item in order.items:
        product = product_map.get(item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product not found: {item.product_id}")
        total_price += product.get("price", 0.0) * item.quantity

    # Step 4: Insert order with calculated total
    order_dict = order.dict(by_alias=True)
    order_dict["total"] = round(total_price, 2)

    result = db.orders.insert_one(order_dict)
    return {"id": str(result.inserted_id)}


# Get orders for a specific user with product lookup and pagination
@router.get("/{user_id}", status_code=200)
def get_orders(user_id: str, limit: int = 10, offset: int = 0):
    db = get_db()

    try:
        cursor = db.orders.find({"user_id": user_id}).skip(offset).limit(limit)
        orders_raw = list(cursor)

        # Step 1: Collect all product_ids from all orders
        all_product_ids = {
            ObjectId(item["product_id"])
            for order in orders_raw
            for item in order.get("items", [])
            if ObjectId.is_valid(item.get("product_id"))
        }

        # Step 2: Fetch products in one go
        product_map = {
            str(product["_id"]): product
            for product in db.products.find({"_id": {"$in": list(all_product_ids)}})
        }

        # Step 3: Attach product details to items
        orders = []
        for order in orders_raw:
            enriched_items = []
            for item in order.get("items", []):
                product = product_map.get(item.get("product_id"))
                if product:
                    enriched_items.append({
                        "productDetails": {
                            "id": str(product["_id"]),
                            "name": product.get("name", "Unknown Product")
                        },
                        "qty": item.get("quantity", 0)
                    })

            orders.append({
                "id": str(order["_id"]),
                "items": enriched_items,
                "total": order.get("total", 0.0)
            })

        return {
            "data": orders,
            "page": {
                "next": offset + limit,
                "limit": limit,
                "previous": max(offset - limit, 0)
            }
        }

    except Exception as e:
        print("Server error:", e)
        raise HTTPException(status_code=500, detail="Something went wrong while fetching orders.")







