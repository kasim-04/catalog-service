from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routers.health import router as health_router
from app.api.routers.genres import router as genres_router
from app.api.routers.countries import router as countries_router
from app.api.routers.persons import router as persons_router
from app.api.routers.movies import router as movies_router
from app.api.routers.admin import router as admin_router

app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
)

# CORS (чтобы фронт мог дергать API)
origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры
app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(genres_router, prefix=settings.api_prefix)
app.include_router(countries_router, prefix=settings.api_prefix)
app.include_router(persons_router, prefix=settings.api_prefix)
app.include_router(movies_router, prefix=settings.api_prefix)
app.include_router(admin_router, prefix=settings.api_prefix)
