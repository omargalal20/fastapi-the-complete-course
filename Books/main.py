import uvicorn
from fastapi import FastAPI

from routers.v1 import books

app = FastAPI()

app.include_router(books.router, prefix="/api/v1", tags=["Books"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
