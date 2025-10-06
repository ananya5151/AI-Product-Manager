from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Assume these modules are defined elsewhere in the project
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"],
    responses={404: {"description": "Task not found"}},
)


@router.patch("/{task_id}", response_model=schemas.TaskRead)
def update_task_completion_status(
    task_id: int,
    task_update: schemas.TaskStatusUpdate,
    db: Session = Depends(get_db),
):
    """
    Update the completion status of a specific task.

    This endpoint uses PATCH for a partial update, specifically targeting the
    `is_completed` field of a task resource.

    Args:
        task_id: The ID of the task to update.
        task_update: The request body containing the new completion status.
                     Expected schema: `{"is_completed": <boolean>}`.
        db: The database session dependency.

    Raises:
        HTTPException: A 404 Not Found error if a task with the specified
                       `task_id` does not exist.

    Returns:
        The fully updated task object, conforming to the `TaskRead` schema.
    """
    # Attempt to retrieve the task from the database
    db_task = crud.task.get(db=db, id=task_id)

    # If the task doesn't exist, return a 404 error
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    # The crud.task.update function is assumed to handle the logic of applying
    # the Pydantic model data to the SQLAlchemy model and committing the session.
    updated_task = crud.task.update(db=db, db_obj=db_task, obj_in=task_update)

    return updated_task
