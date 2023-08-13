# Take-Home Assignment

A python3.11 project for G123 assignment, use FastAPI and Postgres to complete it. Also need docker supported.

## Structure    
    ```
    .
    ├── Dockerfile
    ├── README.md
    ├── alembic
    ├── alembic.ini
    ├── docker-compose.yml
    ├── financial <APIs>
    ├── get_raw_data.py
    ├── main.py
    ├── models.py
    ├── prod.env
    ├── .env
    └── requirements.txt
    ```

## Setting up env by requirement.txt
    Run 
    ```bash
    pip install --no-cache-dir -r requirements.txt
    ```

### Running FastAPI and PostgresSQL by docker-compose.(Recommended)
    Run
    ```bash
    docker-compose up
    ```

## Collectiong stock data from alphavantage.
The `get_raw_data.py` file in root folder, will start collecting data from alphavantage, and store them in db.
    Run 
    ```bash
    python get_raw_data.py
    ```

## Running a Posgres by docker

    Run 
    ```bash
    docker pull Postgres
    docker run -e POSTGRES_PASSWORD=admin$ -p 5432:5432 Postgres
    ```

## Running a FastAPI server, when server started, will automatically collecting data.
    Run (Require Postgres db)
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 5000
    ```

## Migration
    Migrate Postgres with alembic

## env file
    .env for dev
    prod.env for production