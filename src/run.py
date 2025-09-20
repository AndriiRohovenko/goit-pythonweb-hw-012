import uvicorn
from dotenv import load_dotenv
import os


def dev():
    load_dotenv(".env.dev")
    api_host = os.getenv("API_HOST")
    api_port = int(os.getenv("API_PORT"))
    uvicorn.run("src.main:app", host=api_host, port=api_port, reload=True)


def prod():
    load_dotenv(".env")
    api_host = os.getenv("API_HOST")
    api_port = int(os.getenv("API_PORT"))
    uvicorn.run("src.main:app", host=api_host, port=api_port)
