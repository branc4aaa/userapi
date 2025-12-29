from fastapi import FastAPI
from .routes import router as uapi_router
from .db import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(uapi_router)
