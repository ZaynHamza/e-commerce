from fastapi import APIRouter, Depends, File, UploadFile
from models.product import Product
from schemas.product import PostProduct
from routes.auth import authenticate
from tortoise.transactions import in_transaction
from datetime import datetime
import os


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
        return {"success": False,
                "error": "not authenticated"}


@product_router.patch("/products/{product_id}")
async def patch_product(product_id: int, schema: PostProduct, authenticated: dict = Depends(authenticate)):
    if authenticated:
        await Product.filter(id=product_id).update(**schema.__dict__, updated_at=datetime.now())
        return {"success": True}
    else:
        return {"success": False,
                "error": "not authenticated"}


@product_router.delete("/products/{product_id}")
async def delete_product(product_id: int, authenticated: dict = Depends(authenticate)):
    if authenticated:
        await Product.filter(id=product_id).delete()
        return {"success": True}
    else:
        return {"success": False,
                "error": "not authenticated"}


@product_router.get("/products/{product_id}")
async def get_product(product_id: int):
    product = await Product.filter(id=product_id).first()
    return {
        "success": True,
        "product": product
    }


@product_router.patch("/products/{product_id}/image")
async def patch_product_image(product_id: int, image: UploadFile = File(None), authenticated: dict = Depends(authenticate)):
    if authenticated:
        product = await Product.get_or_none(id=product_id)
        if not product:
            return {"success": True,
                    "error": "product not found"}

        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        async with in_transaction() as conn:
            if product.image is not None and product.image != "":
                if product.image:
                    if isinstance(product.image, str):
                        os.remove(product.image)
                product.image = None
                await product.save(using_db=conn)

            if image:
                file_path = f"uploads/{image.filename}"
                with open(file_path, "wb") as f:
                    f.write(image.file.read())
                product.image = file_path
                await product.save(using_db=conn)
            return {"success": True, "message": "Image updated successfully"}

    else:
        return {"success": False, "error": "Not authenticated"}


@product_router.get("/products")
async def get_products():
    products = await Product.all()
    return {
        "success": True,
        "products": products
    }
