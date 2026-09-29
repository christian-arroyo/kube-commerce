from fastapi import FastAPI
from apps.checkout_api.core.logging import setup_logging
from apps.checkout_api.api.v1 import checkout_routes
from apps.checkout_api.db.schema import Base, engine

setup_logging()
# Only do this while developing. In production, the database should be created and migrated using Alembic or another migration tool,
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routes
app.include_router(checkout_routes.router)
