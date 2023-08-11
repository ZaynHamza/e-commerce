from fastapi import APIRouter, Depends, File, UploadFile
from models.product import Product
from schemas.product import PostProduct
from routes.auth import authenticate
from tortoise.transactions import in_transaction
from datetime import datetime
import os
import platform
from uuid import uuid4
import aiofiles


product_router = APIRouter()


# current_dir = os.getcwd()
# db_file_path = os.path.join(current_dir, "db.sqlite3")
#
#
# # function to save file
# async def file_save(file):
#     path_data = current_dir
#     path_data = os.path.join(path_data, 'files')
#     file_name = file.filename
#     file_type = file_name.split('.')
#     file_type = file_type[-1]
#     name = '{}.{}'.format(str(uuid4().hex), file_type)
#     my_path = os.path.join(path_data, name)
#     async with aiofiles.open(my_path, 'wb') as out_file:
#         content = await file.read()  # async read
#         await out_file.write(content)  # async write
#     return {
#         "image_path": '/files/{}'.format(name)
#     }


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


# @product_router.post("/products")
# async def post_product(schema: PostProduct, authenticated: dict = Depends(authenticate), file: UploadFile = File(None)):
#     if authenticated:
#         async with in_transaction() as conn:
#             new = Product(**schema.__dict__)
#             await new.save(using_db=conn)
#
#             # if file is not None:
#
#
#             return {
#                 "success": True,
#                 "id": new.id
#             }
#     else:
#         return {"success": False,
#                 "error": "not authenticated"}


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


@product_router.get("/products")
async def get_products():
    products = await Product.all()
    return {
        "success": True,
        "products": products
    }
