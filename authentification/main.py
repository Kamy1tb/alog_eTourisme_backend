from fastapi import FastAPI
from prisma import Prisma
import uvicorn

from routes.authentification import router as router_authentification



app = FastAPI()

prisma = Prisma()

app.include_router(router_authentification)




@app.get("/api1")
async def read_root():
    return {"Service": "Authentification"}


