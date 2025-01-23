from fastapi import APIRouter
from starlette import status

router = APIRouter(prefix="/auth")


@router.get("", status_code=status.HTTP_200_OK)
def get_user():
    return {'user': 'Authenticated'}
