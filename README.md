# 2d-to-3d-server

## Installation

Install dependencies using `pip install -r requirements.txt`. Pull the TripoSR git submodule using `git pull --recurse-submodules`.

## Running

Run `uvicorn main:app --reload` to run the web app. The `--reload` arg enables live reloading (on file changes).

To test the API using `curl` and a test image (`hamburger.png`), receiving an `.obj`: `curl -X POST -F "image=@hamburger.png" -o "hamburger.obj" http://localhost:8000/upload/`
