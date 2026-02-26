from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()  # No root_path here

latest_txt_data = {"content": None}

class TXTData(BaseModel):
    content: str

@app.post("/upload")
def upload_txt(data: TXTData):
    latest_txt_data["content"] = data.content
    return {"status": "received"}

@app.get("/latest")
def get_latest():
    return latest_txt_data