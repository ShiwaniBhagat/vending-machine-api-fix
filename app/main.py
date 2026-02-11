from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import Base, engine
from app.routers import items, purchase, slots


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Vending Machine API", lifespan=lifespan)

# Include routers with prefixes and tags
app.include_router(slots.router, prefix="/slots", tags=["Slots"])
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(purchase.router, prefix="/purchase", tags=["Purchase"])


@app.get("/health",tags=["Health"])
def health():
    return {"status": "ok"}
