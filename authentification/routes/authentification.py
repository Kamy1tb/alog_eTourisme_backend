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

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "alog.project23@gmail.com"
password = "zejfjrpshsmueymq"





router = APIRouter()


prisma = Prisma()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

secret_key = secrets.token_hex(32)

class SignInOut(BaseModel):
    token: str
    user: object




#vérifier la validité du mail
def is_valid_email(email):
    return validate_email(email)


#envoie du mail de confirmation

async def send_mail(receiver:str):
    context = ssl.create_default_context()
    access_number = random.randint(100000, 999999)
    created = await  prisma.validation_mail.create(
        {
            "email": receiver,
            "token" : access_number
        }
        )
    message = """\
    Subject: E-tourisme app mail validation

    your validation code is :"""+ str(access_number)
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver, message)
    
    return {"state": "mail sent successfully"}


# Verify the user's password
def verify_password(plain_password, hashed_password):
    return (bcrypt.checkpw(plain_password, hashed_password))

async def authenticate_user(mail: str, password: str):
    user =  await prisma.users.find_first(where={"email": mail})
   
    if not user:
        return False
    if not ( password == user.password): 
        return False
    del user.password
    del user.validation_mail
    return SignInOut(token=create_access_token(user,secret_key),user=user)


# Create an access token for the user
def create_access_token(data, secret_key):
    payload = {
        'data': str(data),
        'exp': datetime.utcnow() + timedelta(seconds=10800)
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


@router.on_event("startup")
async def startup():
    await prisma.connect()
@router.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


class SignIn(BaseModel):
    email: str
    password: str

@router.post("/login")

async def login(user : SignIn):
    
    user = await authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect mail or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

class SignUp(BaseModel):
    email: str
    password: str
    fullname: str
    phone: str
    address: str


@router.post("/signup")
async def signup(user: SignUp):
    is_valid = is_valid_email(user.email)
    if is_valid:
        print("L'adresse e-mail est valide.")
        created = await prisma.users.create(
        {
            "email": user.email,
            "password": user.password,                        # bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode(),
            "fullname": user.fullname,
            "phone": user.phone,
            "ISVALID":0,
            "address": user.address
        }
        
    )
        await send_mail(user.email)
        return {"created": user.fullname,
                "state" : "non vérifié"
                }
    else:
        print("L'adresse e-mail n'est pas valide.")
        raise HTTPException(
            status_code=400,
            detail="L'adresse e-mail n'est pas valide.",
            headers={"WWW-SignUp": "Bearer"},
        )
    
@router.get("/state_mail")
async def state_mail(mail:str):
   #TODO
    print("dok nzidha")


class Mail_verif(BaseModel):
    email: str
    token: int
    
    
@router.post("/mail_verification")
async def verify_mail(verif: Mail_verif):

    correct_token = await prisma.validation_mail.find_first(
        where={
            "email" : verif.email
        }
    )

    print(correct_token.token)
    print(verif.token)
    if correct_token.token == verif.token:
        update = await prisma.users.update(
            where={
                "email": verif.email
            },
            data={
                "ISVALID":1
            }
        )
        return {"state" : "mail vérifié avec success"}
    else:
        return {"state": "le numéro introduit est incorrect"}

    