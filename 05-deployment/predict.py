import pickle
from typing import Literal
from pydantic import BaseModel, Field
from fastapi import FastAPI
import uvicorn

class Client(BaseModel):
    lead_source: str
    number_of_courses_viewed: int
    annual_income: float


class PredictResponse(BaseModel):
    pred_converted: float


with open('pipeline_v2.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)

app = FastAPI(title='customer-coverted')

def predict_single(datapoint): 
    result = pipeline.predict_proba(datapoint)[0, 1]
    return float(result)

@app.post("/predict")
def predict(client: Client) -> PredictResponse:
    prob = predict_single(client.model_dump())   

    return PredictResponse(pred_converted=prob)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)