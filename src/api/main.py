import time
import uvicorn
import pybreaker
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from src.agents.memory import get_memory_agent
from src.agents.master_router import llm, supervisor, pretty_print_messages
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
        st = time.time()
        session_id = "default-session"
        memory_agent, memory = get_memory_agent(llm=llm, session_id=session_id)

        for chunk in supervisor.stream({
            "messages": [
                {"role": "user", "content": request.query}
            ]
        }):
            pretty_print_messages(chunk)
        final_message_history = chunk["supervisor"]["messages"]
        print("user: ", request.query)
        print("assistant: ", final_message_history[1].dict()['content'])
        memory.save_context({"input": request.query}, {"output": final_message_history[1].dict()['content']})
        print("memory: ", memory.load_memory_variables({})["chat_history"])
        response = final_message_history[1].dict()['content']

        print(f"time taken {time.time()-st}")
        return PlainTextResponse(response)
    except:
        raise HTTPException(status_code=504, detail="🔴 No response from downstream service (timeout or unreachable).")


@app.post("/query")
def query_endpoint(request: QueryRequest):
    try:
        response = get_agentic_response(request)
        return PlainTextResponse(response)
    except pybreaker.CircuitBreakerError:
        raise HTTPException(status_code=503, detail="🔴 Service temporarily unavailable (circuit open).")
        
if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=6000, reload=True)