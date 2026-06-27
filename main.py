from fastapi import FastAPI
import database
from routers import produtos

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

app.include_router(produtos.router)