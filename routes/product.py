from fastapi import APIRouter, Depends
from models.product import Product
from schemas.product import PostProduct
from routes.auth import authenticate
from tortoise.transactions import in_transaction
from datetime import datetime


product_router = APIRouter()


@product_router.post("/products")
async def post_product(schema: PostProduct, authenticated: dict = Depends(authenticate)):
    if authenticated:
        async with in_transaction() as conn:
            new = Product(**schema.__dict__)
            await new.save(using_db=conn)
            return {
                "success": True,
                "id": new.id
            }
    else:
        return {"error": "not authenticated"}


@product_router.patch("/products/{product_id}")
async def patch_product(product_id: int, schema: PostProduct, authenticated: dict = Depends(authenticate)):
    if authenticated:
        await Product.filter(id=product_id).update(**schema.__dict__, updated_at=datetime.now())
        return {"success": True}
    else:
        return {"error": "not authenticated"}


@product_router.delete("/products/{product_id}")
async def delete_product(product_id: int, authenticated: dict = Depends(authenticate)):
    if authenticated:
        await Product.filter(id=product_id).delete()
        return {"success": True}
    else:
        return {"error": "not authenticated"}


@product_router.get("/products")
async def get_products():
    products = await Product.all()
    return {
        "success": True,
        "products": products
    }
