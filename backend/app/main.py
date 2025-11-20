from fastapi import FastAPI

from app.api.routes import health_router, events_router, findings_router, stats_router
from app.db.base import Base
from app.db.session import engine



def create_app() -> FastAPI:
    app = FastAPI(title="Mini Compliance Monitor")

    app.include_router(health_router , prefix= "/health", tags=["health"])
    app.include_router(events_router , prefix= "/events", tags=["events"])
    app.include_router(findings_router , prefix= "/findings", tags=["findings"])
    app.include_router(stats_router , prefix= "/stats", tags=["stats"])

    return app

app = create_app()  
