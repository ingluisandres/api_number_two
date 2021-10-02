from fastapi import APIRouter
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import schemas
from app.config import database
from app.services import services


router = APIRouter(
    prefix="/v1/usuario",
    tags=["usuario"]
)


@router.post('/', response_model=schemas.Usuario)
def create_usuario(usuario: schemas.Usuario, db: Session=Depends(database.get_db), 
            current_user: schemas.Admin = Depends(services.get_current_user)):
    db_usuario = services.get_usuario_by_email(db=db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail='woops the email is in use')
    return services.create_usuario(db=db, usuario=usuario)

@router.get('/{usuario_id}', response_model=schemas.Usuario)
def read_usuario(
            usuario_id: int, 
            db: Session=Depends(database.get_db), 
            current_user: schemas.Admin = Depends(services.get_current_user)):
    db_usuario = services.get_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(
            status_code=404, detail='sorry this client does not exist'
        )
    return db_usuario

@router.get('/apellido/', response_model=List[schemas.Usuario])
def read_usuarios_by_last_name(
            skip: int=0, 
            limit: int=10, 
            db: Session=Depends(database.get_db), 
            current_user: schemas.Admin = Depends(services.get_current_user)):
    return services.get_usuarios_by_last_name(db=db, skip=skip, limit=limit)

@router.get('/edad/', response_model=List[schemas.Usuario])
def read_usuarios_by_age(
            skip: int=0, 
            limit: int=10, 
            db: Session=Depends(database.get_db), 
            current_user: schemas.Admin = Depends(services.get_current_user)):
    return services.get_usuarios_by_age(db=db, skip=skip, limit=limit)

@router.put('/{usuario_id}', response_model=schemas.Usuario)
def update_usuario(
            usuario_id: int, 
            usuario: schemas.Usuario,
            db: Session = Depends(database.get_db), 
            current_user: schemas.Admin = Depends(services.get_current_user)):
    return services.update_usuario(db=db, post=usuario, usuario_id=usuario_id)

@router.delete('/{usuario_id}')
def delete_client(
            usuario_id: int, 
            db: Session = Depends(database.get_db), 
            current_user: schemas.Admin = Depends(services.get_current_user)):
    db_usuario = services.get_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(
            status_code=404, detail='sorry this usuario does not exist'
        )
    services.delete_usuario(db=db, usuario_id=usuario_id)
    return{'message':f'successfully deleted usuario with id: {usuario_id}'}