from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(root_path="/api")

latest_txt_data = {
    "content":       None,
    "device_name":   None,
    "sampling_rate": None,
    "duration_val":  None,
}

class TXTData(BaseModel):
    content:       str
    device_name:   Optional[str]  = None
    sampling_rate: Optional[int]  = None
    duration_val:  Optional[int]  = None

@app.post("/upload")
def upload_txt(data: TXTData):
    latest_txt_data["content"]       = data.content
    latest_txt_data["device_name"]   = data.device_name
    latest_txt_data["sampling_rate"] = data.sampling_rate
    latest_txt_data["duration_val"]  = data.duration_val
    return {"status": "received"}

@app.get("/latest")
def get_latest():
    return latest_txt_data
