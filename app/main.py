from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Microservicio CRUD Canciones")

app.include_router(router)