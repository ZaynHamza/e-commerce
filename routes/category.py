from fastapi import APIRouter, Depends
from models.product import Category
from schemas.product import PostCategory
from routes.auth import authenticate
from tortoise.transactions import in_transaction
from datetime import datetime

category_router = APIRouter()


@category_router.post("/categories")
async def post_category(schema: PostCategory, authenticated: dict = Depends(authenticate)):
    print("in post ", authenticated)
    if authenticated:
        async with in_transaction() as conn:
            new = Category(name=schema.name)
            await new.save(using_db=conn)
        return {"success": True,
                "id": new.id}
    else:
        return {"success": False,
                "error": "not authenticated"}


@category_router.patch("/categories/{category_id}")
async def patch_category(category_id: int, schema: PostCategory, authenticated: dict = Depends(authenticate)):
    if authenticated:
        await Category.filter(id=category_id).update(name=schema.name, updated_at=datetime.now())
        return {"success": True}
    else:
        return {"success": False,
                "error": "not authenticated"}


@category_router.delete("/categories/{category_id}")
async def delete_category(category_id: int, authenticated: dict = Depends(authenticate)):
    if authenticated:
        await Category.filter(id=category_id).delete()
    else:
        return {"success": False,
                "error": "not authenticated"}


@category_router.get("/categories")
async def get_categories():
    categories = await Category.all()
    return {
        "success": True,
        "categories": categories
    }

