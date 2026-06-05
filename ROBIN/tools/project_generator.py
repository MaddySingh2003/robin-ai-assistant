import subprocess
import os


def create_react_project(project_name="ReactApp"):

    try:

        subprocess.run(
            f"npm create vite@latest {project_name} -- --template react",
            shell=True,
            check=True
        )

        return f"React project created: {project_name}"

    except Exception as e:

        return f"React project error: {e}"


def create_fastapi_project(project_name="FastAPIApp"):

    try:

        os.makedirs(
            project_name,
            exist_ok=True
        )

        main_file = os.path.join(
            project_name,
            "main.py"
        )

        with open(
            main_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
'''from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}
'''
            )

        req = os.path.join(
            project_name,
            "requirements.txt"
        )

        with open(
            req,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "fastapi\nuvicorn"
            )

        return f"FastAPI project created: {project_name}"

    except Exception as e:

        return f"FastAPI error: {e}"


def create_node_project(project_name="NodeApp"):

    try:

        os.makedirs(
            project_name,
            exist_ok=True
        )

        with open(
            os.path.join(
                project_name,
                "index.js"
            ),
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
'''console.log("Hello Node");
'''
            )

        return f"Node project created: {project_name}"

    except Exception as e:

        return f"Node error: {e}"