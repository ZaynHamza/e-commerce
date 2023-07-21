from tortoise.models import Model
from tortoise import fields


class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "category"


class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField(null=True)
    price = fields.FloatField(default=0)
    category = fields.ForeignKeyField("models.Category", null=True)
    image = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "product"
