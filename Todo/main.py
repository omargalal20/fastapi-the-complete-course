import uvicorn
from fastapi import FastAPI

from config.environment import get_environment_variables
from database import database
from models import todo

env = get_environment_variables()

todo.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title=env.APP_NAME,
    version=env.APP_VERSION,
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
