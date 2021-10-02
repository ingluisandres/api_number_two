from sqlalchemy import Column, Integer, String, BIGINT

from app.config.database import Base


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    admin_name =  Column(String(40), index=True)
    password =  Column(String(400), index=True)


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(40), index=True)
    apellido_paterno = Column(String(20), index=True)
    apellido_materno = Column(String(20), index= True)
    edad =  Column(Integer, index= True)
    email = Column(String(40), index=True)
    telefono=  Column(BIGINT, index= True)