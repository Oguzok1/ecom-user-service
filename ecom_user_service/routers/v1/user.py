import fastapi
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

router = fastapi.APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/me")
async def get_me(
    token=Depends(OAuth2PasswordBearer(tokenUrl="token"))
):
    return token
