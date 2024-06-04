from datetime import timedelta, datetime
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, status
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from passlib.context import CryptContext
from app.api.models.users import UserCreate

user_router = APIRouter()
http_bearer = HTTPBearer()
fake_users = [{"name": "Ilka", "email": "Ilka@pisun.ru", "age": 29, "is_subscribed": True}]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Секретный ключ для подписи и верификации токенов JWT
SECRET_KEY = "mysecretkey"  # тут мы в реальной практике используем что-нибудь вроде команды Bash (Linux) 'openssl rand -hex 32', и храним очень защищенно
ALGORITHM = "HS256"  # плюс в реальной жизни мы устанавливаем "время жизни" токена

# Пример информации из БД
USERS_DATA = [
    {"username": "admin", "password": "adminpass"}
]  # в реальной БД мы храним только ХЭШИ паролей (можете прочитать про библиотеку, к примеру, 'passlib') + соль (известная только нам добавка к паролю)

EXPIRATION_TIME = timedelta(minutes=3)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'


USERS_DATA = [
    {"username": "admin", "password": "adminpass", "role": Role.ADMIN.value},
    {"username": "user", "password": "userpass", "role": Role.USER.value},
    {"username": "guest", "password": "userpass", "role": Role.USER.value},
]
for dd in USERS_DATA:
    dd["password"] = pwd_context.hash(dd["password"])


class User(BaseModel):
    username: str
    password: str
    role: str


def authenticate_user(username: str, password: str) -> bool:
    for user in USERS_DATA:
        if user["username"] == username:
            return pwd_context.verify(password, user["password"])
    return False


def create_jwt_token(data: dict):
    data.update({"exp": datetime.utcnow() + EXPIRATION_TIME})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_user_by_token(creds: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = creds.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    for user in USERS_DATA:
        if username in user["username"]:
            return User(**user)


def get_user(username: str):
    pass


@user_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if authenticate_user(username, password):
        return {"access_token": create_jwt_token({"sub": username}), "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@user_router.get("/protected_resource")
async def about_me(creds: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = creds.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})

    return {"message": "Access granted to protected resource", "user": username}


@user_router.post("/create_user")
def create_user(user: User, current_user: User = Depends(get_user_by_token)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    USERS_DATA.append(user)
    return {"status": 200, "message": f"new user added {user}"}


@user_router.get("/users")
def update_user(current_user: User = Depends(get_user_by_token)):
    # if current_user.role != "user" and current_user.role != "admin":
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return USERS_DATA
