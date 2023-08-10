import os
from sqlmodel import Session, create_engine
from sqlalchemy import func, and_
from models import financial_data
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL')


router = APIRouter(prefix="/finance", tags=["finance"])
# create DB if not existed
engine = create_engine(DB_URL)


# @router.on_event("startup")
# def on_startup():
    
#     return
@router.get("/financial_data")
async def get_all_records():
    with Session(engine) as session:
        all_record = session.query(financial_data)
        return all_record