import fastapi
from starlette.responses import RedirectResponse

router = fastapi.APIRouter()


@router.get("/", include_in_schema=False)
def docs():
    return RedirectResponse(url="/docs")


@router.get("/health")
def health():
    return {"status": "ok"}
