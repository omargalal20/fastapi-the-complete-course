import logging

import uvicorn
from fastapi import FastAPI

from config.settings import get_settings
from data.database import postgres
from data.models import todo, user
from routers.v1 import todos, auth, users

settings = get_settings()

todo.Base.metadata.create_all(bind=postgres.engine)
user.Base.metadata.create_all(bind=postgres.engine)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    return response


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(todos.router, prefix="/api/v1", tags=["Todos"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
