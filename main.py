from fastapi import FastAPI
from core.config import settings
from infrastructure.db.session import engine
from infrastructure.db.base import Base
from api.base import api_router
from webapps.base import api_router as webapp_router
from fastapi.staticfiles import StaticFiles


def create_tables():
    Base.metadata.create_all(bind=engine)  # Connects the Fast Api with the database objects


def include_router(app):
    app.include_router(api_router)
    app.include_router(webapp_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def start_application():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    configure_static(app)
    return app


app = start_application()
