import os
import json 
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

def initialize_gemini():
    """Loads API key and configures the Gemini client."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")
    genai.configure(api_key=api_key)
    print("Gemini API initialized successfully for Backend Agent.")

def backend_agent(task_description: str) -> str:
    """
    Generates backend code based on a task description.
    
    Args:
        task_description: A string describing a specific backend task.
        
    Returns:
        A string containing the AI's response in JSON format.
    """
    print(f"Generating backend code for: '{task_description}'")

    # --- PROMPT ENGINEERING FOR FASTAPI/PYTHON ---
    prompt = f"""
    You are an expert Senior Backend Developer specializing in Python with the FastAPI framework.
    Your task is to generate the Python code for a single API endpoint based on the task description below.

    Follow these rules strictly:
    1.  Use FastAPI for all routing and API operations.
    2.  Use Pydantic models for data validation and serialization. Name the schemas clearly (e.g., TaskCreate, TaskRead).
    3.  Include Python type hints and clear docstrings for all functions and models.
    4.  For database operations, assume a SQLAlchemy session is available via FastAPI's dependency injection (`db: Session = Depends(get_db)`).
    5.  Assume necessary models and schemas are defined in `database.py`, `models.py`, and `schemas.py`. You only need to write the router/endpoint logic.

    Task Description:
    ---
    {task_description}
    ---

    IMPORTANT: Your final output must be ONLY a valid JSON object. Do not include any other text, explanations, or markdown fences.
    The JSON object must have two keys:
    1.  `filename`: A suitable filename for the code, following Python conventions (e.g., "task_routes.py").
    2.  `python_code`: A string containing the full, clean Python code for the specified task.

    Example JSON structure:
    {{
      "filename": "auth_routes.py",
      "python_code": "from fastapi import APIRouter, Depends\\n\\nrouter = APIRouter()\\n\\n@router.post('/login')\\ndef login():\\n    return {{'message': 'Login successful'}}"
    }}
    """
    
    # --- API CALL ---
    model = genai.GenerativeModel('models/gemini-pro-latest')
    response = model.generate_content(prompt)
    
    return response.text

# This block allows us to test the script directly
if __name__ == "__main__":
    try:
        initialize_gemini()
        
        # Define a sample backend task for testing
        sample_task = "Create a REST API endpoint: `POST /api/tasks` to create a new task and store it in the database."
        
        # Call the backend agent with the sample task
        print("\n--- Running Backend Agent ---")
        raw_output = backend_agent(sample_task)
        
        # --- PARSE AND SAVE THE OUTPUT ---
        print("\n--- Parsing and Saving Code ---")
        
        # Clean the string by removing markdown fences
        cleaned_json_str = raw_output.strip().replace("```json", "").replace("```", "").strip()
        
        try:
            # Convert the cleaned string into a Python dictionary
            code_data = json.loads(cleaned_json_str)
            
            # Extract the code parts
            filename = code_data["filename"]
            python_code = code_data["python_code"]
            
            # ---- CORRECTED FILE SAVING LOGIC ----
            # Define the base directory for all backend code
            base_output_dir = Path("output/backend")
            
            # The filename from the AI might include subdirectories (e.g., "api/routes/tasks.py")
            # so we join it with our base path.
            file_path = base_output_dir / filename
            
            # CRITICAL FIX: Ensure the file's specific parent directory exists *before* writing the file.
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the code to the file
            file_path.write_text(python_code, encoding="utf-8")
            
            print(f"✅ Successfully saved code to: {file_path}")

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error: Failed to parse JSON or find expected keys. {e}")
            print("Raw response was:")
            print(raw_output)

    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")