# Synapse: Multi-Agent Orchestration System

## Overview
Synapse is a sophisticated multi-agent orchestration system that leverages FastAPI, LangChain, and LangGraph to coordinate multiple specialized AI agents. The system employs a supervisor-based architecture to route tasks to appropriate specialized agents and synthesize their outputs into coherent responses.

## Features
- **Supervisor Architecture**: Centralized task coordination and orchestration
- **Specialized Agents**:
  - Search Agent: Handles information retrieval tasks
  - Intent Agent: Analyzes user intent and emotion
  - Instruction Agent: Processes and executes specific instructions
  - Conversation Agent: Manages conversation flow and context
  - Memory Agent: Maintains chat history and context retrieval
- **Caching System**: Implements response caching for improved performance
- **Circuit Breaker Pattern**: Ensures system resilience with automatic failure handling
- **API Interface**: RESTful API built with FastAPI

## Technical Stack
- FastAPI for API development
- LangChain for AI agent framework
- LangGraph for agent supervision
- Together AI for language model integration
- PyBreaker for circuit breaker implementation
- Redis/Cache system for response optimization

## Setup
1. Clone the repository
2. Create a `.env` file with the following variables:
   ```
   TOGETHER_API_KEY=your_key_here
   TAVILY_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   ```
3. Install dependencies using uv:
   ```bash
   uv sync
   ```

## Usage
1. Start the server:
   ```bash
   make run
   ```
2. The API will be available at `http://127.0.0.1:6000`
3. Send POST requests to `/query` endpoint with JSON body:
   ```json
   {
     "query": "your query here"
   }
   ```

## Architecture
The system uses a supervisor-based architecture where:
1. User queries are received through the FastAPI endpoint
2. The supervisor agent analyzes the query and routes it to appropriate specialized agents
3. Agents process their specific tasks in parallel when possible
4. Results are synthesized into a final response
5. Responses are cached for future use

## Error Handling
- Circuit breaker pattern prevents system overload
- Automatic failover with configurable retry settings
- Proper error status codes and messages
- Timeout handling for downstream services

## Performance Optimization
- Response caching system
- Parallel agent execution when possible
- Circuit breaker for system protection
- Configurable timeout settings