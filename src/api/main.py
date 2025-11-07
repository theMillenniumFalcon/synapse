import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_endpoint(request: QueryRequest):
    try:
        response = "Hello, World!"
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=6000, reload=True)