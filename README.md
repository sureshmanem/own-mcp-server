# Own MCP Server

A local file-access MCP (Model Context Protocol) server built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk). It exposes tools that let AI assistants (such as GitHub Copilot, Claude, etc.) **list and read files** from a designated safe directory on your machine.

---

## Features

| Tool | Description |
|------|-------------|
| `list_files` | Lists all files in the configured safe directory |
| `read_file_content` | Reads and returns the contents of a specific file |

- **Directory-traversal protection** — paths are resolved to absolute form and checked against the safe root before any read is performed.
- **Configurable safe directory** — change the `SAFE_DIRECTORY` variable in `server.py` (defaults to `~/Downloads/mydata`).

---

## Prerequisites

- **Python** ≥ 3.12
- **uv** — fast Python package manager ([install guide](https://docs.astral.sh/uv/getting-started/installation/))

---

## Installation

```bash
# Clone the repo
git clone https://github.com/sureshmanem/own-mcp-server.git
cd own-mcp-server

# Create a virtual environment and install dependencies
uv sync
```

This installs the `mcp[cli]` package and all other dependencies specified in `pyproject.toml`.

---

## Configuration

### 1. Safe Directory

Open `server.py` and update `SAFE_DIRECTORY` to the folder you want to expose:

```python
SAFE_DIRECTORY = os.path.expanduser("~/Downloads/mydata")
```

> **Warning:** Only expose directories you trust. The server allows any connected AI client to read files inside this folder.

### 2. VS Code / GitHub Copilot

Add the server to your **VS Code MCP settings** (`.vscode/mcp.json` or User `mcp.json`):

```jsonc
{
  "servers": {
    "my-local-files": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--directory", "/absolute/path/to/own-mcp-server",
        "mcp", "run", "server.py"
      ]
    }
  }
}
```

> Replace `/absolute/path/to/own-mcp-server` with the actual path to this project folder.

---

## Usage

### Run Standalone

```bash
uv run mcp run server.py
```

The server starts on **stdio** and waits for MCP messages from a connected client.

### Run with MCP Inspector (for debugging)

```bash
uv run mcp dev server.py
```

This opens an interactive inspector UI where you can invoke tools and see requests/responses.

### Example Prompts (in Copilot Chat / Claude)

Once the server is connected, you can ask your AI assistant:

- *"List the files in my local folder"*
- *"Read the contents of notes.txt"*

---

## Project Structure

```
own-mcp-server/
├── server.py          # MCP server — defines tools (list_files, read_file_content)
├── main.py            # Standalone entry point (hello-world placeholder)
├── pyproject.toml     # Project metadata & dependencies
├── .python-version    # Pinned Python version (3.12)
├── .gitignore         # Git ignore rules
├── uv.lock            # Locked dependency versions
└── README.md          # This file
```

---

## Security Considerations

- The server only allows access to files inside `SAFE_DIRECTORY`.
- A directory-traversal guard prevents `../` attacks.
- **Do not** expose sensitive directories (home folder root, `/etc`, etc.).
- The server is designed for **local development use only** — do not expose it to the network.

---

## License

This project is provided as-is for personal/educational use. Add a `LICENSE` file to specify your preferred license.
