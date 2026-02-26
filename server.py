from mcp.server.fastmcp import FastMCP
import os

# Initialize the server
mcp = FastMCP("LocalFiles")

# Set a root directory you want to allow access to
# WARNING: Only expose folders you trust!
SAFE_DIRECTORY = os.path.expanduser("~/Downloads/mydata")

@mcp.tool()
def list_files() -> list[str]:
    """List all files in the safe directory."""
    if not os.path.exists(SAFE_DIRECTORY):
        return [f"Directory {SAFE_DIRECTORY} does not exist."]
    return os.listdir(SAFE_DIRECTORY)

@mcp.tool()
def read_file_content(filename: str) -> str:
    """Read the contents of a specific file in the safe directory."""
    # Simple security check to prevent directory traversal
    path = os.path.join(SAFE_DIRECTORY, filename)
    
    if not os.path.abspath(path).startswith(os.path.abspath(SAFE_DIRECTORY)):
        return "Error: Access denied (outside of safe directory)."
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

if __name__ == "__main__":
    mcp.run()