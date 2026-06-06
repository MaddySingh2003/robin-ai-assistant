import os
import subprocess


# =====================================
# OPEN IN VSCODE
# =====================================


import os

def get_projects_folder():

    desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )

    projects = os.path.join(
        desktop,
        "ROBIN_Projects"
    )

    os.makedirs(
        projects,
        exist_ok=True
    )

    return projects

def open_vscode(path):

    try:

        subprocess.Popen(
            f'code "{path}"',
            shell=True
        )

    except Exception as e:

        print("VSCode error:", e)

# =====================================
# REACT PROJECT
# =====================================


def create_react_project(project_name="ReactApp"):

    try:

        root = get_projects_folder()

        project_path = os.path.join(
            root,
            project_name
        )

        subprocess.run(
            [
                r"C:\Program Files\nodejs\npx.cmd",
                "create-vite@latest",
                project_name,
                "--template",
                "react",
                "--skip-install"
            ],
            cwd=root,
            check=True
        )

        open_vscode(project_path)

        return (
            f"React project created at "
            f"{project_path}"
        )

    except Exception as e:

        return f"React project error: {e}"

def create_fastapi_project(
    project_name="FastAPIApp"
):

    try:

        root = get_projects_folder()

        project_path = os.path.join(
            root,
            project_name
        )

        app_dir = os.path.join(
            project_path,
            "app"
        )

        os.makedirs(
            app_dir,
            exist_ok=True
        )

        with open(
            os.path.join(
                app_dir,
                "main.py"
            ),
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

        with open(
            os.path.join(
                project_path,
                "requirements.txt"
            ),
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
'''fastapi
uvicorn
'''
            )

        open_vscode(project_path)

        return (
            f"FastAPI project created at "
            f"{project_path}"
        )

    except Exception as e:

        return f"FastAPI error: {e}"

# =====================================
# NODE EXPRESS PROJECT
# =====================================

def create_node_project(
    project_name="NodeApp"
):

    try:

        os.makedirs(
            project_name,
            exist_ok=True
        )

        with open(
            os.path.join(
                project_name,
                "server.js"
            ),
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
'''const express = require("express");

const app = express();

app.get("/", (req,res)=>{
    res.send("Hello World");
});

app.listen(3000);
'''
            )

        open_vscode(project_name)

        return f"Node project created: {project_name}"

    except Exception as e:

        return f"Node error: {e}"


# =====================================
# NEXTJS PROJECT
# =====================================

def create_nextjs_project(
    project_name="NextApp"
):

    try:

        subprocess.run(
            [
                "npx",
                "create-next-app@latest",
                project_name,
                "--yes"
            ],
            check=True
        )

        open_vscode(project_name)

        return f"NextJS project created: {project_name}"

    except Exception as e:

        return f"NextJS error: {e}"


# =====================================
# FLASK PROJECT
# =====================================

def create_flask_project(
    project_name="FlaskApp"
):

    try:

        os.makedirs(
            project_name,
            exist_ok=True
        )

        with open(
            os.path.join(
                project_name,
                "app.py"
            ),
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
'''from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Flask"

if __name__ == "__main__":
    app.run(debug=True)
'''
            )

        open_vscode(project_name)

        return f"Flask project created: {project_name}"

    except Exception as e:

        return f"Flask error: {e}"


# =====================================
# PYTHON CLI PROJECT
# =====================================

def create_python_project(
    project_name="PythonApp"
):

    try:

        os.makedirs(
            project_name,
            exist_ok=True
        )

        with open(
            os.path.join(
                project_name,
                "main.py"
            ),
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
'''def main():
    print("Hello Python")

if __name__ == "__main__":
    main()
'''
            )

        open_vscode(project_name)

        return f"Python project created: {project_name}"

    except Exception as e:

        return f"Python error: {e}"


# =====================================
# C++ PROJECT
# =====================================

def create_cpp_project(
    project_name="CppProject"
):

    try:

        os.makedirs(
            project_name,
            exist_ok=True
        )

        with open(
            os.path.join(
                project_name,
                "main.cpp"
            ),
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
'''#include <iostream>

int main() {
    std::cout << "Hello C++";
    return 0;
}
'''
            )

        open_vscode(project_name)

        return f"C++ project created: {project_name}"

    except Exception as e:

        return f"C++ error: {e}"


# =====================================
# JAVA MAVEN PROJECT
# =====================================

def create_java_project(
    project_name="JavaApp"
):

    try:

        src = os.path.join(
            project_name,
            "src"
        )

        os.makedirs(
            src,
            exist_ok=True
        )

        with open(
            os.path.join(
                src,
                "Main.java"
            ),
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
'''public class Main {

    public static void main(String[] args) {
        System.out.println("Hello Java");
    }
}
'''
            )

        open_vscode(project_name)

        return f"Java project created: {project_name}"

    except Exception as e:

        return f"Java error: {e}"