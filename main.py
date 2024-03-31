from io import BytesIO
import os
import sys

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import numpy as np
from PIL import Image
from rembg import remove
import torch
from torchvision.transforms.functional import center_crop

sys.path.append("TripoSr")
from tsr.system import TSR

model = TSR.from_pretrained("stabilityai/TripoSR", config_name="config.yaml", weight_name="model.ckpt")
model.renderer.set_chunk_size(8192)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.post("/crop_resize_image/")
async def crop_resize_image(image: UploadFile = File(...)):
  filename = os.path.splitext(image.filename)[0]  # Strip extension
  contents = await image.read()
  image = Image.open(BytesIO(contents))

  image = center_crop(image, min(image.size)).resize((1024, 1024))  # Center crop and resize image for Stability AI API
  image.save(os.path.join("cache", f"{filename}.png"))
  
  return FileResponse(os.path.join("cache", f"{filename}.png"), media_type='application/octet-stream', filename=f"{filename}.png")


@app.post("/convert_2d_to_3d/")
async def convert_2d_to_3d(image: UploadFile = File(...)):
  filename = os.path.splitext(image.filename)[0]  # Strip extension
  contents = await image.read()
  image = np.array(Image.open(BytesIO(contents)).convert("RGB"))

  image = remove(image).astype(np.float32) / 255.0  # Remove background (alpha) and cast to float
  image = image[:, :, :3] * image[:, :, 3:4] + (1 - image[:, :, 3:4]) * 0.5  # Convert from RGBA to RGB with gray background

  scene_codes = model([image], device='cpu')
  meshes = model.extract_mesh(scene_codes, resolution=256)
  meshes[0].export(os.path.join("cache", f"{filename}.obj"))
  
  return FileResponse(os.path.join("cache", f"{filename}.obj"), media_type='application/octet-stream', filename=f"{filename}.obj")
