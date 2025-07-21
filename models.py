from pydantic import BaseModel, Field, validator
from typing import List


# Product Size Model
class SizeModel(BaseModel):
    size: str = Field(..., min_length=1, description="Size must be a non-empty string")
    quantity: int = Field(..., ge=0, description="Quantity must be 0 or greater")


# Product Model
class ProductModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Product name is required and cannot be empty")
    sizes: List[SizeModel] = Field(..., min_items=1, description="At least one size is required")
    price: float = Field(..., ge=0, description="Price must be a non-negative number")



# Order Item Model
class OrderItem(BaseModel):
    product_id: str = Field(..., min_length=24, max_length=24, description="Product ID must be a valid 24-character hex ObjectId")
    quantity: int = Field(..., ge=1, description="Quantity must be at least 1")


# Order Model
class OrderModel(BaseModel):
    user_id: str = Field(..., min_length=1, description="User ID is required")
    items: List[OrderItem] = Field(..., min_items=1, description="At least one item must be in the order")
    total: float = Field(..., ge=0, description="Total amount must be a non-negative value")

