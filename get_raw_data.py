import logging
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from models import financial_data
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

API_KEY = os.getenv('API_KEY')
DB_URL = os.getenv('DB_URL')

# create DB if not existed
engine = create_engine(DB_URL)
SQLModel.metadata.create_all(engine)

query_url = 'https://www.alphavantage.co/query'

def getStackData(function_name, symbol):
  params = { 'function': function_name, 'symbol': symbol, 'apikey': API_KEY, 'outputsize': 'compact' }
  r = requests.get(query_url, params = params)
  data = r.json()
  # check data is matched, or throw error
  if data['Meta Data']['2. Symbol'] != symbol:
    raise ValueError('Symbol not matched!')
  else:
    # print(data)
    return data
def formatRaw(raw_data):
  #   {
  #     "symbol": "IBM",
  #     "date": "2023-02-14",
  #     "open_price": "153.08",
  #     "close_price": "154.52",
  #     "volume": "62199013",
  # },
  formated_data = []
  symbol = raw_data['Meta Data']['2. Symbol']
  for key, value in raw_data['Time Series (Daily)'].items():
    formated_data.append({'symbol': symbol, 'date': key, 'open_price': value['1. open'], 'close_price': value['4. close'], 'volume': value['5. volume']})
  return formated_data
def saveToDB(data):
  with Session(engine) as session:
    for record in data:
      date = datetime.strptime(record['date'], '%Y-%m-%d')
      # check if data is existed
      exist = session.query(financial_data).filter(financial_data.date == date).filter(financial_data.symbol == record['symbol'] ).first()
      if exist:
          logging.info("record is already existed")
      else:
        finance_record = financial_data(
            symbol=record['symbol'],
            date=date,
            open_price=record['open_price'],
            close_price=record['close_price'],
            volume=record['volume'],
        )

        try:
            session.add(finance_record)
            session.commit()
            session.refresh(finance_record)
            logging.info('Inserted success')
        except SQLAlchemyError as error:
            session.rollback()
            raise error

try:
  ibm_raw_data = getStackData('TIME_SERIES_DAILY', 'IBM')
  apple_raw_data = getStackData('TIME_SERIES_DAILY', 'AAPL')
  ibm_formattedData = formatRaw(ibm_raw_data)
  saveToDB(ibm_formattedData)
  apple_formattedData = formatRaw(apple_raw_data)
  saveToDB(apple_formattedData)

except ValueError as err:
  print(err.args)

