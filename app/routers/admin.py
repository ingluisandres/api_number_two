from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schemas import schemas
from app.services import services
from app.config import database


router = APIRouter(
    prefix="/v1/admin",
    tags=["admin"]
)


@router.post('/newadmin', response_model=schemas.ShowAdmin)
def create_admin(admin: schemas.Admin, db: Session=Depends(database.get_db)):
    return services.create_admin(db=db, admin=admin)

@router.get('/', response_model=schemas.ShowAdmin)
def get_admin(current_user: schemas.Admin= Depends(services.get_admin)):
    return current_user