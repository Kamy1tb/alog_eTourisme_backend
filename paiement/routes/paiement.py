from fastapi import FastAPI, HTTPException, Depends,APIRouter, Form
from prisma import Prisma
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Any
import stripe
from torch import device
from fastapi.responses import RedirectResponse

router = APIRouter()


prisma = Prisma()


stripe.api_key="sk_test_51NCLddERPpRCu3V3Wnnpoj2eymGnlYBgULFVSz9FKHPQGKrqMAcSLBgDTp8a6BO40ode8cZL19OC4Zi4VH1CJ74r00jgY4IDbu"

@router.on_event("startup")
async def startup():
    await prisma.connect()
@router.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


class SignIn(BaseModel):
    email: str
    password: str

@router.get("/api2/checkout_session")
async def checkout():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price' : 'price_1NCz1hERPpRCu3V3wqZqJ8z9',
                    'quantity': 1,
                }
                   
            ],
            mode="payment"  ,
            success_url= "http://localhost:8000/success_payment",
            cancel_url="http://localhost:8000/failure_payment"
        )
    except Exception as e:
        return str(e)
    
    return RedirectResponse(checkout_session.url)



@router.get("/api2/success_payment")
async def success():
   
    
    return {"statut" : "payment validé"}
 
@router.get("/cancel_payment")
async def cancel():
   
    
    return {"statut" : "payment annulé"}