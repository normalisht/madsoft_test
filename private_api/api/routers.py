from fastapi import APIRouter

from private_api.api.endpoints import s3_router

main_router = APIRouter()
main_router.include_router(s3_router, tags=['s3'])
