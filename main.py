from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from financial import api

from get_raw_data import init

init()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")

