from fastapi import FastAPI
import database
from routers import products
from modules.users import router as users

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

app.include_router(products.router)
app.include_router(users.router)