from fastapi import FastAPI
from prisma import Prisma
import uvicorn

from routes.paiement import router as router_paiment



app = FastAPI()

prisma = Prisma()

app.include_router(router_paiment)




@app.get("/")
async def read_root():
    return {"Service": "Paiement"}


