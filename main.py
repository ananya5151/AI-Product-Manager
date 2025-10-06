import json
from pathlib import Path
import time

# Import the main functions from our agent files
from coordinator_agent import coordinator_agent, initialize_gemini
from frontend_agent import frontend_agent
from backend_agent import backend_agent

def main():
    """
    The main function to orchestrate the multi-agent system.
    """
    try:
        initialize_gemini()
    except ValueError as e:
        print(e)
        return

    project_brief = """
    Build a simple task management application. 
    Users need to see a list of tasks, add new tasks via a form, and mark tasks as complete by clicking a checkbox.
    This requires a frontend UI and a backend API with a database to persist the tasks.
    """
    
    print("--- 🚀 Starting AI Project Generation ---")
    print(f"Project Brief: '{project_brief.strip()[:80]}...'")

    # --- 1. RUN COORDINATOR AGENT ---
    print("\n--- [1/3] Running Coordinator Agent to get the project plan ---")
    raw_plan_output = coordinator_agent(project_brief)
    
    try:
        # Clean and parse the coordinator's output
        cleaned_plan_str = raw_plan_output.strip().replace("```json", "").replace("```", "").strip()
        plan_data = json.loads(cleaned_plan_str)
        print("✅ Plan received and parsed successfully.")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Error: Failed to parse the project plan. Cannot proceed. {e}")
        return

    # --- 2. RUN FRONTEND AGENT ---
    print("\n--- [2/3] Running Frontend Agent for each task ---")
    frontend_tasks = plan_data.get("frontend_tasks", [])
    if not frontend_tasks:
        print("No frontend tasks found.")
    else:
        for i, task in enumerate(frontend_tasks, 1):
            print(f"\nProcessing Frontend Task ({i}/{len(frontend_tasks)}): {task}")
            try:
                raw_code_json = frontend_agent(task)
                cleaned_code_str = raw_code_json.strip().replace("```json", "").replace("```", "").strip()
                code_data = json.loads(cleaned_code_str)

                component_name = code_data["component_name"]
                tsx_code = code_data["tsx_code"]
                css_code = code_data["css_code"]
                
                output_dir = Path(f"output/frontend/components/{component_name}")
                output_dir.mkdir(parents=True, exist_ok=True)
                
                (output_dir / f"{component_name}.tsx").write_text(tsx_code, encoding="utf-8")
                (output_dir / f"{component_name}.module.css").write_text(css_code, encoding="utf-8")
                
                print(f"✅ Code for '{component_name}' saved successfully.")
                time.sleep(1) # Brief pause to avoid overwhelming the API
            except Exception as e:
                print(f"❌ Error processing frontend task '{task}': {e}")

    # --- 3. RUN BACKEND AGENT ---
    print("\n--- [3/3] Running Backend Agent for each task ---")
    backend_tasks = plan_data.get("backend_tasks", [])
    if not backend_tasks:
        print("No backend tasks found.")
    else:
        for i, task in enumerate(backend_tasks, 1):
            print(f"\nProcessing Backend Task ({i}/{len(backend_tasks)}): {task}")
            try:
                raw_code_json = backend_agent(task)
                cleaned_code_str = raw_code_json.strip().replace("```json", "").replace("```", "").strip()
                code_data = json.loads(cleaned_code_str)

                filename = code_data["filename"]
                python_code = code_data["python_code"]
                
                base_output_dir = Path("output/backend")
                file_path = base_output_dir / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(python_code, encoding="utf-8")
                
                print(f"✅ Code for '{filename}' saved successfully.")
                time.sleep(1) # Brief pause to avoid overwhelming the API
            except Exception as e:
                print(f"❌ Error processing backend task '{task}': {e}")
    
    print("\n--- ✅ All tasks complete! Project generated successfully in the 'output' directory. ---")


if __name__ == "__main__":
    main()