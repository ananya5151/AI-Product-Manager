from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

# --- Assumed Imports ---
# The following are assumed to be defined in your project structure.
# from database import engine  # Your SQLAlchemy engine instance
# from models import Base       # Your declarative base from SQLAlchemy models

# This is a placeholder for demonstration since we can't import real files.
# In a real application, you would remove this and use the imports above.
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
# --- End of Placeholders ---

router = APIRouter(
    prefix="/admin/database",
    tags=["Database Management"],
)

class StatusResponse(BaseModel):
    """Schema for a simple status message response."""
    message: str


@router.post(
    "/initialize",
    status_code=status.HTTP_201_CREATED,
    response_model=StatusResponse,
    summary="Initialize Database Tables",
    description="Creates all database tables based on the SQLAlchemy models. "
                "This endpoint should only be used for initial setup or in "
                "controlled development environments."
)
def initialize_database():
    """
    Initializes the database by creating all necessary tables.

    This function iterates through all the metadata that SQLAlchemy's declarative
    base has collected and issues `CREATE TABLE` statements to the database
    for any tables that do not already exist.

    **Warning**: This is a powerful operation that modifies the database schema.
    It should not be exposed publicly in a production environment without
    strong authentication and authorization controls.
    """
    try:
        # The `create_all` method is idempotent. It checks for the existence
        # of tables before attempting to create them.
        Base.metadata.create_all(bind=engine)
        return {"message": "Database tables created successfully."}
    except Exception as e:
        # Catches potential database connection errors or other SQLAlchemy issues.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while initializing the database: {str(e)}",
        )
