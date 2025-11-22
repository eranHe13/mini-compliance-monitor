from fastapi import FastAPI

from app.api.routes import health_router, events_router, findings_router, stats_router
from app.db.base import Base
from app.db.session import engine

from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()
def create_app() -> FastAPI:
    app = FastAPI(title="Mini Compliance Monitor")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],        # אפשר גם ["*"] לפיתוח בלבד
        allow_credentials=True,
        allow_methods=["*"],          # מאפשר GET/POST/OPTIONS וכו'
        allow_headers=["*"],          # מאפשר כל headers (Authorization וכו')
    )
    app.include_router(health_router , prefix= "/health", tags=["health"])
    app.include_router(events_router , prefix= "/events", tags=["events"])
    app.include_router(findings_router , prefix= "/findings", tags=["findings"])
    app.include_router(stats_router , prefix= "/stats", tags=["stats"])

    return app

app = create_app()  
