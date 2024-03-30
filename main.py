from io import BytesIO
import os
import sys

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import numpy as np
from PIL import Image
from rembg import remove
import torch

sys.path.append("TripoSr")
from tsr.system import TSR

model = TSR.from_pretrained("stabilityai/TripoSR", config_name="config.yaml", weight_name="model.ckpt")
model.renderer.set_chunk_size(8192)

app = FastAPI()


@app.post("/upload/")
async def convert_2d_image_to_3d(image: UploadFile = File(...)):
  filename = os.path.splitext(image.filename)[0]  # Strip extension
  contents = await image.read()
  image = np.array(Image.open(BytesIO(contents)).convert("RGB"))
  image = remove(image).astype(np.float32) / 255.0  # Remove background (alpha) and cast to float
  image = image[:, :, :3] * image[:, :, 3:4] + (1 - image[:, :, 3:4]) * 0.5  # Convert from RGBA to RGB with gray background

  scene_codes = model([image], device='cpu')
  meshes = model.extract_mesh(scene_codes, resolution=256)
  meshes[0].export(os.path.join("cache", f"{filename}.obj"))
  
  return FileResponse(os.path.join("cache", f"{filename}.obj"), media_type='application/octet-stream', filename=f"{filename}.obj")
