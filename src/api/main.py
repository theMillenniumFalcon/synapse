import uvicorn
import pybreaker
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

breaker = pybreaker.CircuitBreaker(
    fail_max=3,             # max failures before opening circuit
    reset_timeout=10        # time (seconds) to wait before trying again (half-open)
)

class QueryRequest(BaseModel):
    query: str

@breaker
def get_agentic_response(request: QueryRequest):
    try:
        response = "Hello, World!"
        return response
    except:
        raise HTTPException(status_code=504, detail="🔴 No response from downstream service (timeout or unreachable).")

@app.post("/query")
def query_endpoint(request: QueryRequest):
    try:
        response = get_agentic_response(request)
        return response
    except pybreaker.CircuitBreakerError:
        raise HTTPException(status_code=503, detail="🔴 Service temporarily unavailable (circuit open).")
        
if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=6000, reload=True)