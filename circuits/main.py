from fastapi import FastAPI
from prisma import Prisma
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


from routes.circuits import router as router_circuits



app = FastAPI()

prisma = Prisma()

app.include_router(router_circuits)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8003"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/api3")
async def read_root():
    return {"Service": "circuits"}


