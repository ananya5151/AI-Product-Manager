# AI Product Manager: A Multi-Agent AI System for Code Generation

## Project Overview

This project is a multi-agent AI system designed to automate the process of software development from a project brief to generated code. It utilizes Google's Gemini API to power a hierarchy of specialized AI agents, coordinated by a central "Product Manager" agent. The system accepts a high-level project description, breaks it down into frontend and backend tasks, and delegates the code generation to the respective agents, which then write and save the code files.

---

## Core Features

- **Coordinator Agent:** Ingests a project brief, analyzes it, and decomposes it into a structured JSON plan of frontend and backend tasks.
- **Frontend Agent:** An expert in React and TypeScript. It takes a single frontend task and generates the code for a `.tsx` component and its corresponding `.module.css` file.
- **Backend Agent:** An expert in Python and FastAPI. It takes a single backend task and generates the code for API endpoints, including Pydantic schemas and database interaction patterns.
- **Orchestration:** A main entry point (`main.py`) that manages the end-to-end workflow, from planning to code generation and file saving.

---

## Technology Stack

- **AI Engine:** Google Gemini API (`gemini-pro-latest`)
- **Programming Language:** Python 3.8+
- **Core AI Library:** `google-generativeai`
- **Environment Management:** `python-dotenv`, `venv`

---

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ananya5151/AI-Product-Manager.git](https://github.com/ananya5151/AI-Product-Manager.git)
    cd AI-Product-Manager
    ```

2.  **Set up the environment:**
    ```bash
    # Create a virtual environment
    python -m venv venv
    # Activate it (Windows)
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your API Key:**
    - Create a file named `.env` in the root directory.
    - Add your Google Gemini API key to it:
      ```
      GEMINI_API_KEY="YOUR_API_KEY_HERE"
      ```

5.  **Run the system:**
    - Modify the `project_brief` variable in `main.py` with your project idea.
    - Execute the main script:
      ```bash
      python main.py
      ```
    - All generated code will be saved in the `output/` directory.
