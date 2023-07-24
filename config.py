import os
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import auth_router
from routes.product import product_router
from routes.category import category_router
from routes.order import order_router

current_dir = os.getcwd()
db_file_path = os.path.join(current_dir, "db.sqlite3")

if not os.path.exists(db_file_path):
    open(db_file_path, 'a').close()


def create_app() -> FastAPI:
    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
    register_tortoise(
        app,
        db_url=f'sqlite://{current_dir}/db.sqlite3',
        modules={'models': ["models.order", "models.product", "models.auth"]},
        generate_schemas=True,
        add_exception_handlers=True
    )
    register_views(app=app)
    # connect socketio to app
    # app.mount("/", socket_router)
    return app


def register_views(app: FastAPI):
    app.include_router(auth_router, tags=['Auth'])
    app.include_router(product_router, tags=['Product'])
    app.include_router(category_router, tags=['Category'])
    app.include_router(order_router, tags=['Order'])


TORTOISE_ORM = {
    "connections": {
        "default": f'sqlite://{current_dir}/db.sqlite3'
    },
    "apps": {
        "models": {
            "models": [
                "models.order", "models.product", "models.auth"
            ],
            "default_connection": "default",
        },
    },
}
