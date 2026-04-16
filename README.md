# Pro-Gamer-Tracker MCP Server

A demonstration of the **Model Context Protocol (MCP)** — a standard that lets AI assistants like Claude directly interact with your data and systems through well-defined tools.

This server manages a game player database backed by MongoDB, exposing it as MCP tools that any compatible AI client can call naturally in conversation.

---

## What is MCP?

The **Model Context Protocol** is an open standard that bridges AI models and external data sources. Instead of copy-pasting data into a chat window, you define **tools** and **resources** once — and the AI can invoke them on demand.

This project shows how simple it is to wrap an existing database with MCP, turning it into a live, queryable backend for an AI assistant.

---

## What This Server Does

The server exposes a MongoDB player database through 7 MCP tools:

| Tool | Description |
| ---- | ----------- |
| `get_player` | Retrieve a player's full profile document |
| `add_new_player` | Insert a new player with default stats |
| `update_xp` | Update a player's XP value |
| `level_up_player` | Set a player's level |
| `add_achievement` | Push a new achievement into a player's history |
| `get_leaderboard` | Return the top 10 players ranked by XP |
| `duel_players` | Simulate a turn-based duel between two players |

It also exposes a **MCP Resource** at `player://{username}` for direct profile lookups.

---

## Requirements

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- MongoDB running locally on `mongodb://localhost:27017/`

### Python dependencies

```text
mcp[cli] >= 1.26.0
pymongo  >= 4.16.0
httpx    >= 0.28.1
```

---

**Note:** If you are on MacOS, you do not have to follow the instructions provided at the link for
[uv](https://docs.astral.sh/uv/). Instead you can just use brew install. This makes it so you do not need root
permissions to install the program.

```bash
brew install uv
```

To install mongodb for MacOS:

```bash
brew tap mongodb/brew
brew install mongodb-community
```

## Setup & Running

### 1. Install dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or using pip:

```bash
pip install "mcp[cli]>=1.26.0" "pymongo>=4.16.0" "httpx>=0.28.1"
```

### 2. Start MongoDB

Make sure a MongoDB instance is running locally:

```bash
mongod
```

Or use a MongoDB Atlas connection string — update line 7 in [server.py](server.py):

```python
client = MongoClient("your-atlas-connection-string")
```

### 3. Run the MCP server

**Development mode** (with MCP Inspector UI):

```bash
mcp dev server.py
```

**Direct execution:**

```bash
python server.py
```

---

## Connecting to Claude Desktop

Add this to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "pro-gamer-tracker": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/memo-mcp"
    }
  }
}
```

Once connected, Claude can answer questions like:

- *"Who are the top 10 players right now?"*
- *"Add a new player called Zephyr and give them the achievement 'First Blood'."*
- *"Simulate a duel between Alice and Bob."*

---

## Project Structure

```text
memo-mcp/
├── server.py        # MCP server — tools and resources
├── pyproject.toml   # Project metadata and dependencies
└── README.md
```
