from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Assume these are defined in their respective files
# from .. import models, schemas
# from ..database import get_db

# For demonstration purposes, we'll define placeholder classes here
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# --- Placeholder Schemas (schemas.py) ---
class TaskBase(BaseModel):
    """Base Pydantic model for a Task, containing shared fields."""
    title: str = Field(
        ..., 
        min_length=3, 
        max_length=100, 
        description="The title of the task."
    )
    description: Optional[str] = Field(
        None, 
        max_length=500, 
        description="An optional description of the task."
    )
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    """Pydantic model for creating a new task. Used for request body validation."""
    pass

class TaskRead(TaskBase):
    """Pydantic model for reading a task. Used for response serialization."""
    id: int
    is_completed: bool

    class Config:
        from_attributes = True # formerly orm_mode

# --- Placeholder Models and DB (models.py, database.py) ---
# This is a mock setup to make the example runnable without a full project structure.
# In a real application, you would import these from other files.
class Task:
    def __init__(self, **kwargs):
        self.id = 1
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.due_date = kwargs.get("due_date")
        self.is_completed = False

class DBSession:
    def query(self, *args, **kwargs):
        return self
    def filter(self, *args, **kwargs):
        return self
    def first(self):
        return None # Simulate no existing task by default
    def add(self, *args, **kwargs): pass
    def commit(self): pass
    def refresh(self, obj, *args, **kwargs):
        # Simulate DB assigning an ID and default values
        setattr(obj, 'id', 1)
        setattr(obj, 'is_completed', False)

def get_db():
    """Dependency to get a DB session."""
    yield DBSession()

# --- API Router ---

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
) -> Task:
    """
    Creates a new task after validating the incoming data.

    FastAPI automatically validates the request body against the `TaskCreate` schema.
    If the data is invalid (e.g., title is too short, or a field has the wrong type),
    a 422 Unprocessable Entity error is returned automatically.

    This endpoint also includes business logic validation to prevent duplicate titles.

    Args:
        task_data: The validated task data from the request body.
        db: The database session dependency.

    Raises:
        HTTPException: A 400 Bad Request error if a task with the same title already exists.

    Returns:
        The newly created task object.
    """
    # Business logic validation: check for a unique title
    existing_task = db.query(Task).filter(Task.title == task_data.title).first()
    if existing_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A task with the title '{task_data.title}' already exists.",
        )

    # Create a new SQLAlchemy model instance from the validated Pydantic data
    db_task = Task(**task_data.model_dump())

    # Add to session, commit to DB, and refresh to get new data like the ID
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task
