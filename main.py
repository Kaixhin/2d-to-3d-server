from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()


@app.post("/upload/")
async def upload_image(image: UploadFile = File(...)):
  contents = await image.read()
  with open(image.filename, "wb") as f:
    f.write(contents)
  return FileResponse(image.filename, media_type='application/octet-stream', filename=image.filename)
