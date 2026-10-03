from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Historical Mystery Book Cover API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    id: int
    title: str
    status: str
    score: float
    timestamp: str

# In-memory seed data
data_store = [
    {"id": 1, "title": "The Silent Archive", "status": "pending", "score": 8.5, "timestamp": datetime.now().isoformat()},
    {"id": 2, "title": "Shadows of Versailles", "status": "approved", "score": 9.2, "timestamp": datetime.now().isoformat()}
]

@app.get("/api/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/api/analytics", response_model=List[Review])
def get_analytics():
    return data_store

@app.post("/api/reviews", response_model=Review)
def submit_review(review: Review):
    data_store.append(review.dict())
    return review

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)