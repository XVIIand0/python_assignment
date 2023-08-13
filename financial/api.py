import os
from sqlmodel import Session, create_engine, select
from sqlalchemy import func
from models import financial_data
from fastapi import APIRouter
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

DB_URL = os.getenv('DB_URL')


router = APIRouter()
# create DB if not existed
engine = create_engine(DB_URL)


# @router.on_event("startup")
# def on_startup():
    
#     return
@router.get("/financial_data/all")
async def get_all_records():
    with Session(engine) as session:
        all_record = session.query(financial_data).all()
        return all_record
@router.get("/financial_data")
async def get_records_by_conditions(start_date: str | None = None, end_date: str | None = None, symbol: str | None = None, limit: int | None = 5, page: int | None = 1):
    with Session(engine) as session:
        statement = select(financial_data)
        where_array = []
        if start_date:
            st_date = datetime.strptime(start_date, '%Y-%m-%d')
            where_array.append(financial_data.date >= st_date)
        if end_date:
            ed_date = datetime.strptime(end_date, '%Y-%m-%d')
            where_array.append(financial_data.date <= ed_date)
        if symbol:
            where_array.append(financial_data.symbol == symbol)

        counts = session.exec(select([func.count(financial_data.id)]).where(*where_array)).one()
        total_pages = counts // limit
        if (counts % limit) > 0:
            total_pages += 1
        error = ''
        # count offset
        if page > total_pages:
            error = "Out of pages!"
        current_offest = (page - 1) * limit


        statement = statement.where(*where_array).offset(current_offest).limit(limit)
    
        results = session.exec(statement).all()

        response = {
            "data": results,
            "pagination": {
                "count": counts,
                "page": page,
                "limit": limit,
                "pages": total_pages
            },
            "info": {
                'error': error
            }
        }
        return response
@router.get("/statistics")
async def get_statistics(start_date: str, end_date: str , symbol: str):
    with Session(engine) as session:
        # get avg data by sql cmd
        statement = select(func.avg(financial_data.open_price).label('average_daily_open_price'), func.avg(financial_data.close_price).label('average_daily_close_price'), func.avg(financial_data.volume).label('average_daily_volume'))
        where_array = []
        error = ''
        if start_date:
            st_date = datetime.strptime(start_date, '%Y-%m-%d')
            where_array.append(financial_data.date >= st_date)
        if end_date:
            ed_date = datetime.strptime(end_date, '%Y-%m-%d')
            where_array.append(financial_data.date <= ed_date)
        if symbol:
            where_array.append(financial_data.symbol == symbol)


        statement = statement.where(*where_array)
    
        results = session.exec(statement).all()
        data = {}
        data['start_date'] = start_date
        data['end_date'] = end_date
        data['symbol'] = symbol
        data['average_daily_open_price'] = results[0]['average_daily_open_price']
        data['average_daily_close_price'] = results[0]['average_daily_close_price']
        data['average_daily_volume'] = results[0]['average_daily_volume']

        response = {
            "data": data,
            "info": {
                'error': error
            }
        }
        return response