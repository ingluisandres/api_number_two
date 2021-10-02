from typing import List, Optional
from pydantic import BaseModel


class Usuario(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    edad: int
    email: str
    telefono: int
    class Config():
        orm_mode = True


class Admin(BaseModel):
    admin_name: str
    password: str
    class Config():
        orm_mode = True
    
class ShowAdmin(BaseModel):
    id: int
    admin_name: str
    class Config():
        orm_mode = True


class Login(BaseModel):
    admin_name: str
    password: str
    class Config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    tocken_type: str

class TokenData(BaseModel):
    admin_name: Optional[str] = None    