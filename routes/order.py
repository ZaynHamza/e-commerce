from fastapi import APIRouter, Depends
from models.order import Order, OrderItem
from models.product import Product
from schemas.order import PostOrder
from routes.auth import authenticate
from tortoise.transactions import in_transaction
from datetime import datetime


order_router = APIRouter()


@order_router.post("/orders")
async def post_order(schema: PostOrder):
    async with in_transaction() as conn:
        new_order = Order(client_name=schema.client_name, client_phone=schema.client_phone,
                          client_address=schema.client_address)
        await new_order.save(using_db=conn)

        total_price = 0

        for item in schema.items:
            product_price = await Product.filter(id=item.product_id).first().values('price')
            if product_price is not None:
                total_price += product_price['price'] * item.quantity
                new_order_item = OrderItem(product_id=item.product_id, quantity=item.quantity, order_id=new_order.id)
                await new_order_item.save(using_db=conn)
            else:
                return {"success": False,
                        "error": "product not found"}

        await Order.filter(id=new_order.id).update(total_price=total_price)

    return {"success": True,
            "id": new_order.id}



