from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.schemas import schemas
from app.config import database, models


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/login/")


def get_admin(db: Session=Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        admin = db.query(models.Admin).get(payload["sub"])
    except:
        raise HTTPException(status_code=401, detail="Invalid Email or Password")
    return db.query(models.Admin).filter(models.Admin.admin_name == payload["sub"]).first()

def create_admin(db: Session, admin: schemas.Admin):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(admin.password)
    db_admin = models.Admin(
        admin_name= admin.admin_name,
        password=hashed_password
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def login(db: Session, admin: schemas.Login):
    admin = db.query(models.Admin).filter(models.Admin.admin_name == admin.username).first()
    return admin

def verify_password(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(data, credentials_exception)

def verify_token(data:str, credentials_exception):
    try:
        payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
        admin_name: str = payload.get("sub")
        if admin_name is None:
            raise credentials_exception
        token_data = schemas.TokenData(admin_name=admin_name)
    except JWTError:
        raise credentials_exception


def get_usuario_by_email(db: Session, email:str):
    return db.query(models.Usuario).filter(models.Usuario.email==email).first()

def create_usuario(db: Session, usuario: schemas.Usuario):
    db_usuario = models.Usuario(
            nombre= usuario.nombre, 
            apellido_paterno=usuario.apellido_paterno, 
            apellido_materno=usuario.apellido_materno, 
            edad=usuario.edad,
            email=usuario.email, 
            telefono=usuario.telefono)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuario(db: Session, usuario_id:int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def update_usuario(
        db: Session, 
        post:schemas.Usuario, 
        usuario_id:int):
    db_usuario=get_usuario(db=db, usuario_id=usuario_id)
    # Change the elements
    db_usuario.nombre = post.nombre
    db_usuario.apellido_paterno = post.apellido_paterno
    db_usuario.apellido_materno = post.apellido_materno
    db_usuario.edad = post.edad
    db_usuario.email = post.email
    db_usuario.telefono = post.telefono
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id:int):
    db.query(models.Usuario).filter(models.Usuario.id == usuario_id).delete()
    db.commit()


def get_usuarios_by_last_name(db:Session, skip:int, limit:int):
    temp = db.query(models.Usuario).offset(skip).limit(limit).all()
    #temp[0].apellido_paterno
    array = temp
    for i in range(len(array)):
        for j in range(len(array)):
            if (array[j].apellido_paterno>array[i].apellido_paterno):
                array[i], array[j] = array[j], array[i]
    return array

def get_usuarios_by_age(db:Session, skip:int, limit:int):
    temp = db.query(models.Usuario).offset(skip).limit(limit).all()
    #temp[0].edad
    array = temp
    return merge_sort(array)


def merge(left, right):
    result = []
    x, y = 0,0
    while x < len(left) and y < len(right):
        if(left[x].edad<=right[y].edad):
            result.append(left[x])
            x+=1
        else: 
            result.append(right[y])
            y+=1
    if left:
        result.extend(left[x:])
    if right:
        result.extend(right[y:])
    return result    

def merge_sort(array):
    if len(array) <= 1:
        return array

    middle = len(array) // 2
    left = array[:middle]
    right = array[middle:]

    left = merge_sort(left)
    right = merge_sort(right)
    return list(merge(left, right))