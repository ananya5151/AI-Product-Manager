from fastapi import APIRouter
from .. import schemas  # Assuming a Message schema is defined in schemas.py

router = APIRouter(
    tags=["Root"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_model=schemas.Message,
    summary="Root Endpoint / Health Check",
    description="A simple endpoint to confirm that the backend server is initialized and running correctly."
)
def read_root() -> schemas.Message:
    """
    Check if the API is running.

    This endpoint provides a simple health check for the application,
    returning a welcome message if the server is operational.

    Returns:
        A JSON object with a welcome message confirming the server is running.
    """
    return {"message": "Welcome to the FastAPI Backend! The server is running."}
