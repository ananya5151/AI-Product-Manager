import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

def initialize_gemini():
    """Loads API key and configures the Gemini client."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")
    genai.configure(api_key=api_key)
    print("Gemini API initialized successfully.")

def coordinator_agent(project_brief: str) -> str:
    """
    Analyzes the project brief and decomposes it into tasks using the Gemini API.
    
    Args:
        project_brief: A string containing the user's project description.
        
    Returns:
        A string containing the AI's response in JSON format.
    """
    print(f"Received project brief. Analyzing and decomposing...")

    # --- PROMPT ENGINEERING ---
    # We instruct the AI on its role, the format of the output, and the task to perform.
    prompt = f"""
    You are an expert AI Product Manager. Your role is to analyze a project brief
    and break it down into a structured list of actionable tasks for a software development team.

    Analyze the following project brief and decompose it into two lists of tasks:
    1.  `frontend_tasks`: Specific tasks for a frontend developer (e.g., creating React components).
    2.  `backend_tasks`: Specific tasks for a backend developer (e.g., creating API endpoints, database schemas).

    The project brief is as follows:
    ---
    {project_brief}
    ---

    IMPORTANT: Your final output must be ONLY a valid JSON object, with no other text before or after it.
    The JSON object should have two keys: "frontend_tasks" and "backend_tasks", where each key holds a list of strings.

    Example format:
    {{
      "frontend_tasks": [
        "Create a responsive navigation bar component.",
        "Design a user login form component with email and password fields."
      ],
      "backend_tasks": [
        "Set up a database schema for a 'users' table.",
        "Create a REST API endpoint for user authentication."
      ]
    }}
    """

    # --- API CALL ---
    # Initialize the model and generate the content
    model = genai.GenerativeModel('models/gemini-pro-latest')
    response = model.generate_content(prompt)
    
    # For now, we'll return the raw text. We'll parse it in the next step.
    return response.text

# This block allows us to test the script directly
if __name__ == "__main__":
    # 1. Initialize the Gemini client
    try:
        initialize_gemini()
        
        # 2. Define a sample project brief for testing
        sample_brief = """
        Build a simple task management application. 
        I need a frontend where users can see a list of tasks, add new tasks, and mark tasks as complete. 
        I also need a backend with a database to store the tasks.
        """
        
        # 3. Call the coordinator agent with the sample brief
        print("\n--- Running Coordinator Agent ---")
        raw_output = coordinator_agent(sample_brief)
        
        # 4. Clean and Parse the AI's output
        print("\n--- Parsing Agent's Output ---")
        
        # Clean the string by removing markdown fences and stripping whitespace
        cleaned_json_str = raw_output.strip().replace("```json", "").replace("```", "").strip()
        
        try:
            # Convert the cleaned string into a Python dictionary
            tasks_data = json.loads(cleaned_json_str)
            
            print("Successfully parsed JSON.")
            
            # 5. Neatly print the decomposed tasks
            print("\n--- Decomposed Tasks ---")
            
            print("\n[ Frontend Tasks ]")
            for task in tasks_data.get("frontend_tasks", []):
                print(f"- {task}")
                
            print("\n[ Backend Tasks ]")
            for task in tasks_data.get("backend_tasks", []):
                print(f"- {task}")
                
            print("\n------------------------")
            
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the AI's response.")
            print("Raw response was:")
            print(raw_output)

    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")