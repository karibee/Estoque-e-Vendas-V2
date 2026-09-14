from fastapi import FastAPI
import database
from modules.users import router as users
from modules.products import router as products

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

app.include_router(products.router)
app.include_router(users.router)