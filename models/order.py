from tortoise.models import Model
from tortoise import fields


class Order(Model):
    id = fields.IntField(pk=True)
    client_name = fields.TextField()
    client_phone = fields.TextField()
    client_address = fields.TextField()
    date = fields.DatetimeField(auto_now_add=True)
    total_price = fields.FloatField(default=0)

    class Meta:
        table = "order"


class OrderItem(Model):
    id = fields.IntField(pk=True)
    order = fields.ForeignKeyField("models.Order")
    product = fields.ForeignKeyField("models.Product")
    quantity = fields.IntField(default=1)

    class Meta:
        table = "order_item"
