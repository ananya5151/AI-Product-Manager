from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Tasks"],
)

@router.post(
    "/tasks",
    response_model=schemas.TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task"
)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db)
) -> schemas.TaskRead:
    """
    Create a new task.

    This endpoint adds a new task to the database with the provided title and
    optional description.

    Args:
        task_in: A Pydantic schema with the task's creation data.
        db: The database session, injected by FastAPI.

    Returns:
        The newly created task, serialized as a TaskRead schema.
    """
    # The crud.create_task function handles the database interaction.
    db_task = crud.create_task(db=db, task=task_in)
    return db_task
