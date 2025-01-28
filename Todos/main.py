import uvicorn
from fastapi import FastAPI

from Todos.config.settings import get_settings
from Todos.data.database import postgres
from Todos.data.models import todo, user
from Todos.routers.v1 import todos, auth, users

settings = get_settings()

todo.Base.metadata.create_all(bind=postgres.engine)
user.Base.metadata.create_all(bind=postgres.engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(todos.router, prefix="/api/v1", tags=["Todos"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
