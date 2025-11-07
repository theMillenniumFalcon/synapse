from langchain_ollama import ChatOllama
from langgraph_supervisor import create_supervisor
import os 
import time
from dotenv import load_dotenv
from langchain_together import ChatTogether
load_dotenv()
from src.agents.memory import get_memory_agent
st = time.time()


llm = ChatTogether(
    model="meta-llama/Llama-3-8b-chat-hf",
    max_retries=2,
    api_key=os.getenv("TOGETHER_API_KEY")
)

memory_agent, _ = get_memory_agent(llm, session_id="default-session")

llm2 = ChatOllama(
    model="llama3:8b"
)


def pretty_print_messages(msg_chunk):
    for msg in msg_chunk.get("messages", []):
        role = msg.get("role", "unknown")
        print(f"{role}: {msg['content']}")

supervisor = create_supervisor(
    model=llm,
    agents=[memory_agent],
    prompt=(
        "You are a supervisor managing one agent:\n"
        "- a memory agent. Assign task to retrieve relevant chat history/context"
        " Give the final output answer by getting all the results from all agents and return it to the user."
        "Assign agents in parallel.\n"
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()