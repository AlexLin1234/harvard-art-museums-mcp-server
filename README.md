# Harvard Art Museums MCP Server

A Model Context Protocol (MCP) server that provides access to the [Harvard Art Museums API](https://harvardartmuseums.org/collections/api), giving access to over 224,000+ artworks, artist records, and museum objects.

## Features

This MCP server provides 5 tools for interacting with Harvard's art collection:

- **search_objects** - Search artworks in the collection with filters
- **get_object** - Fetch detailed information about a specific artwork by ID
- **search_people** - Search for artists and people in the collection
- **get_person** - Fetch detailed information about a specific person by ID
- **random_object** - Get a random artwork with optional classification/culture filters

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/AlexLin1234/harvard-art-museums-mcp-server
   cd harvard-art-museums
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install mcp requests python-dotenv pydantic
   ```

3. Get your free API key from https://harvardartmuseums.org/collections/api

4. Create a `.env` file in the project root:
   ```bash
   HARVARD_ART_MUSEUMS_API_KEY=your_api_key_here
   ```

## Configuration

### Claude Desktop

Add this configuration to your Claude Desktop config file:

**MacOS/Linux**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "harvard-art-museums": {
      "command": "python",
      "args": ["/absolute/path/to/harvard-art-museums/server.py"],
      "env": {
        "HARVARD_ART_MUSEUMS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Note**: Make sure to use the absolute path to `server.py` and include your virtual environment's Python if needed:
- Windows: `"C:\\Users\\YourName\\path\\to\\harvard-art-museums\\.venv\\Scripts\\python.exe"`
- MacOS/Linux: `"/Users/YourName/path/to/harvard-art-museums/.venv/bin/python"`

### Other MCP Clients

For other MCP-compatible clients, configure the server with:
- **Command**: Path to Python executable (preferably from the virtual environment)
- **Arguments**: Path to `server.py`
- **Environment**: Set `HARVARD_ART_MUSEUMS_API_KEY` to your API key

## Usage Examples

Once connected to Claude Desktop, you can ask questions like:

- "Search for impressionist paintings by Monet"
- "Find me a random Japanese artwork"
- "Tell me about Pablo Picasso"
- "Show me details about object ID 299843"

## API Rate Limits

The Harvard Art Museums API has the following limits:
- 2,500 requests per day per API key
- Please use responsibly and cache results when possible

## Development

The server uses:
- **MCP SDK** for Model Context Protocol implementation
- **Requests** for HTTP API calls
- **Pydantic** for data validation
- **python-dotenv** for environment variable management

## License

This project is open source and available under the MIT License.

## Resources

- [Harvard Art Museums API Documentation](https://github.com/harvardartmuseums/api-docs)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
