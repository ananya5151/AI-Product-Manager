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
    print("Gemini API initialized successfully for Frontend Agent.")

def frontend_agent(task_description: str) -> str:
    """
    Generates frontend code based on a task description.
    
    Args:
        task_description: A string describing a specific frontend task.
        
    Returns:
        A string containing the AI's response in JSON format.
    """
    print(f"Generating frontend code for: '{task_description}'")

    # --- PROMPT ENGINEERING FOR REACT/TYPESCRIPT ---
    prompt = f"""
    You are an expert Senior Frontend Developer specializing in React and TypeScript.
    Your task is to generate the code for a single React functional component based on the task description below.

    Follow these rules strictly:
    1.  Use modern functional components with React Hooks.
    2.  Use TypeScript for all prop definitions. Define props in an `interface` named `Props`.
    3.  Use CSS Modules for styling. The generated CSS should be a placeholder, but functional.
    4.  The component file should be self-contained.

    Task Description:
    ---
    {task_description}
    ---

    IMPORTANT: Your final output must be ONLY a valid JSON object. Do not include any other text, explanations, or markdown fences.
    The JSON object must have three keys:
    1.  `component_name`: A suitable PascalCase name for the component (e.g., "TaskItem").
    2.  `tsx_code`: A string containing the full code for the React component (`.tsx` file).
    3.  `css_code`: A string containing the placeholder CSS code for the component's CSS Module (`.module.css` file).

    Example JSON structure:
    {{
      "component_name": "MyComponent",
      "tsx_code": "import React from 'react';\\nimport styles from './MyComponent.module.css';\\n...",
      "css_code": ".container {{ \\n  background-color: #f0f0f0;\\n }}"
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
        
        # Define a sample frontend task for testing
        sample_task = "Create a 'TaskItem' component to represent a single task, including its title and a completion checkbox."
        
        # Call the frontend agent with the sample task
        print("\n--- Running Frontend Agent ---")
        raw_output = frontend_agent(sample_task)
        
        # --- PARSE AND SAVE THE OUTPUT ---
        print("\n--- Parsing and Saving Code ---")
        
        # Clean the string by removing markdown fences
        cleaned_json_str = raw_output.strip().replace("```json", "").replace("```", "").strip()
        
        try:
            # Convert the cleaned string into a Python dictionary
            code_data = json.loads(cleaned_json_str)
            
            # Extract the code parts
            component_name = code_data["component_name"]
            tsx_code = code_data["tsx_code"]
            css_code = code_data["css_code"]
            
            # Create the output directory if it doesn't exist
            output_dir = Path(f"output/frontend/components/{component_name}")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Define the full file paths
            tsx_file_path = output_dir / f"{component_name}.tsx"
            css_file_path = output_dir / f"{component_name}.module.css"
            
            # Write the code to the files
            tsx_file_path.write_text(tsx_code, encoding="utf-8")
            css_file_path.write_text(css_code, encoding="utf-8")
            
            print(f"✅ Successfully saved code to: {output_dir}")
            print(f"   - {tsx_file_path.name}")
            print(f"   - {css_file_path.name}")

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error: Failed to parse JSON or find expected keys. {e}")
            print("Raw response was:")
            print(raw_output)

    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")