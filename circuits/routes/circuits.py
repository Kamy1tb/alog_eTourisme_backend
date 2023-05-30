from fastapi import FastAPI, HTTPException, Depends,APIRouter, Form
from prisma import Prisma
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Any
import secrets
import bcrypt
from validate_email_address import validate_email
import smtplib, ssl
import jwt
import random



router = APIRouter()


prisma = Prisma()

@router.on_event("startup")
async def startup():
    await prisma.connect()
@router.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()



@router.get("/api3/agences")
async def getAgences():
    agences = await prisma.agence.find_many(

    )
    return agences


@router.get("/api3/circuitsByAgence")
async def circuits(id_agence:int):
    circuits = await prisma.circuit.find_first(    
        where={
            "id_agence": id_agence
        },    
        include={"circuit_activit_": {
                
                "include": {
                    "activit_": True
                }
            },

            "circuit_point": {
                
                "include": {
                    "point_interet": True
                }
            }
            
            
            })
    return circuits