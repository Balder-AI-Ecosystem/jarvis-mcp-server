# jarvis-mcp-server
 
MCP (Model Context Protocol) server bridging external clients (VS Code Copilot, Claude Desktop, etc.) and the JARVIS core API.
 
## Architecture
 
```
Client (VS Code / Claude Desktop)
        │  stdio or HTTP/SSE
        ▼
┌───────────────────────┐
│   jarvis-mcp-server   │
│  (MCP server layer)   │
│  tools/               │
│    chat.py            │
│    autonomy.py        │
│    memory.py          │
│    runtime.py         │
└──────────┬────────────┘
           │  HTTP (localhost:8000)
           ▼
┌───────────────────────┐
│   JARVIS Core API     │
│   (apps/api.py)       │
│   POST /chat          │
│   GET  /autonomy/*    │
│   GET  /chat/history  │
│   GET  /health        │
└───────────────────────┘
```
 
## Installation
 
```bash
cd D:\Autobot\jarvis-mcp-server
python -m venv venv
venv\Scripts\activate
pip install -e .
```
 
## Running
 
```bash
# Stdio transport (used for VS Code / Claude Desktop)
jarvis-mcp
 
# Or directly
python -m jarvis_mcp
```
 
## Configuration
 
Create a `.env` file in this directory:
 
```env
JARVIS_CORE_URL=http://localhost:8000
JARVIS_MCP_TRANSPORT=stdio
JARVIS_REQUEST_TIMEOUT=120
```
 
## VS Code Integration
 
The `.vscode/mcp.json` file is already provided; VS Code will automatically recognize it when opening this directory.
 
## Claude Desktop Integration
 
Add to `claude_desktop_config.json`:
 
```json
{
  "mcpServers": {
    "jarvis": {
      "command": "D:\\Autobot\\jarvis-mcp-server\\venv\\Scripts\\python.exe",
      "args": ["-m", "jarvis_mcp"],
      "env": {
        "JARVIS_CORE_URL": "http://localhost:8000"
      }
    }
  }
}
```
 
## Exposed Tools
 
| Tool | Description |
|------|-------|
| `jarvis_chat` | Send a message to JARVIS and receive a response |
| `jarvis_chat_history` | Retrieve recent conversation history |
| `jarvis_health` | Check the JARVIS core status |
| `jarvis_autonomy_status` | View the status of autonomy cycles |
| `jarvis_autonomy_run` | Manually trigger an autonomy cycle |
| `jarvis_knowledge_search` | Search within the External Brain |
| `jarvis_runtime_preflight` | Run system preflight checks |
