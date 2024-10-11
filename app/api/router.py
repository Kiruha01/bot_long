from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def read_root(r: Request) -> dict:
    print(r.query_params)
    return {"Hello": "World"}


@router.post("/wh")
async def readw_root(r: Request) -> dict:
    print(await r.body())
    return {"Hello": "World"}
