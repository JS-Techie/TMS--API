from dotenv import load_dotenv
load_dotenv()



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os



host=os.getenv("HOST")
port= int(os.getenv("PORT"))



app=FastAPI()



origins=[
    "*"
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials= True,
    allow_methods= ['*'],
    allow_headers= ['*']
)







@app.get("/")
async def root():
    return{'message':'Transport Management System ROOT'}
