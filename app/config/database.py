from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.security.security import MYSQL_ROOT_PASSWORD


SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://root:{MYSQL_ROOT_PASSWORD}@database:3306/usuarios'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./app/config/database.db'
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False}
# )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_database():
    return Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()