from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import backend_pre_start, initial_data
from app.api.api_v1.api import api_router
from app.core.config import settings

backend_pre_start.init()
initial_data.init()

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.CURRENT_API_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.CURRENT_API_STR)
