# 2d-to-3d-server

## Installation

Install dependencies using `pip install -r requirements.txt`. Pull the TripoSR git submodule using `git pull --recurse-submodules`.

## Running

Run `uvicorn main:app --host 0.0.0.0 --port 8000 --reload` to run the web app and make it accessible on the local network. The `--reload` arg enables live reloading (on file changes).

To test the API using `curl` and a test image (`hamburger.png`):
- Center crop and resize image: `curl -X POST -F "image=@hamburger.jpg" -o "hamburger.png" http://<IP>:8000/crop_resize_image/`
- Convert image to 3D .obj file: `curl -X POST -F "image=@hamburger.png" -o "hamburger.obj" http://<IP>:8000/convert_2d_to_3d/`
