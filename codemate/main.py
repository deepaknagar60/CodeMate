import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
from app.controllers import controller

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

app.include_router(controller.router)



if __name__ == "__main__":
    uvicorn.run("main:app",port=8001, reload=True) 