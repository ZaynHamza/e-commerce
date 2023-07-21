from fastapi import APIRouter, HTTPException, Depends, status, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from tortoise.transactions import in_transaction
from models.auth import User
import jwt
from datetime import datetime, timedelta


auth_router = APIRouter()
security = HTTPBasic()


@auth_router.post("/register")
async def register(username: str, password: str):
    async with in_transaction():
        try:
            user = User(username=username)
            await user.set_password(password)
            await user.save()
            return {"message": "User registered successfully!"}
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=400, detail="Failed to register user")


# async def authenticate(credentials: HTTPBasicCredentials = Depends()):
#     user = await User.filter(username=credentials.username).first()
#     if user and user.verify_password(credentials.password):
#         return True
#     else:
#         return False


async def authenticate(token: str = Depends(HTTPBearer())):
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET_KEY, algorithms=['HS256'])
        return True
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


JWT_SECRET_KEY = "your-secret-key"


# def generate_access_token(username: str) -> str:
#     payload = {"username": username}
#     token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
#     return token


def create_access_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm='HS256')
    return token


@auth_router.post("/login")
# async def login(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
#     # Perform user authentication here, and if successful:
#     access_token = create_access_token({"sub": credentials.username})
#     return {"access_token": access_token, "token_type": "bearer"}
async def login(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    user = await User.filter(username=credentials.username).first()
    if user and user.verify_password(credentials.password):
        access_token = create_access_token({"sub": credentials.username})
        response = {"access_token": access_token, "token_type": "bearer"}
        headers = {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
        return JSONResponse(content=response, headers=headers, media_type="application/json; charset=utf-8",
                            status_code=200)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")



