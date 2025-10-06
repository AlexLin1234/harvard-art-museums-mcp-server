import os
import requests
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------
API_BASE = "https://api.harvardartmuseums.org"
API_KEY = os.getenv("HARVARD_ART_MUSEUMS_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "Missing HARVARD_ART_MUSEUMS_API_KEY. Get one at https://api.harvardartmuseums.org/"
    )

# -----------------------------------------------------------------------------
# MODELS
# -----------------------------------------------------------------------------
class Image(BaseModel):
    baseimageurl: Optional[str] = None
    iiifbaseuri: Optional[str] = None
    alttext: Optional[str] = None

class ObjectRecord(BaseModel):
    id: int
    title: Optional[str]
    culture: Optional[str]
    classification: Optional[str]
    dated: Optional[str]
    medium: Optional[str]
    technique: Optional[str]
    url: Optional[str]
    primaryimageurl: Optional[str]
    images: Optional[List[Image]] = None
    people: Optional[List[Dict[str, Any]]] = None

# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def build_url(path: str, params: Dict[str, Any] = {}) -> str:
    url = f"{API_BASE}{path}"
    all_params = {"apikey": API_KEY}
    all_params.update({k: v for k, v in params.items() if v is not None})
    return url, all_params

def get_json(path: str, params: Dict[str, Any] = {}) -> Any:
    url, full_params = build_url(path, params)
    r = requests.get(url, params=full_params, timeout=15)
    r.raise_for_status()
    return r.json()

# -----------------------------------------------------------------------------
# SERVER
# -----------------------------------------------------------------------------
server = Server("harvard-art-museums-mcp")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_objects",
            description="Search artworks in Harvard Art Museums.",
            inputSchema={
                "type": "object",
                "properties": {
                    "q": {"type": "string", "description": "Search query"},
                    "size": {"type": "integer", "default": 10},
                    "page": {"type": "integer", "default": 1},
                    "hasimage": {"type": "boolean", "default": True}
                },
                "required": ["q"]
            }
        ),
        Tool(
            name="get_object",
            description="Fetch a single object by id.",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "Object ID"}
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="search_people",
            description="Search artist/person records.",
            inputSchema={
                "type": "object",
                "properties": {
                    "q": {"type": "string", "description": "Search query"},
                    "size": {"type": "integer", "default": 10},
                    "page": {"type": "integer", "default": 1}
                },
                "required": ["q"]
            }
        ),
        Tool(
            name="get_person",
            description="Fetch a person record by id.",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "Person ID"}
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="random_object",
            description="Return a random object with optional filters.",
            inputSchema={
                "type": "object",
                "properties": {
                    "classification": {"type": "string"},
                    "culture": {"type": "string"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[Any]:
    if name == "search_objects":
        data = get_json("/object", {
            "q": arguments["q"],
            "size": arguments.get("size", 10),
            "page": arguments.get("page", 1),
            "hasimage": int(arguments.get("hasimage", True))
        })
        return [{"type": "text", "text": str(data)}]

    elif name == "get_object":
        data = get_json(f"/object/{arguments['id']}")
        return [{"type": "text", "text": str(data)}]

    elif name == "search_people":
        data = get_json("/person", {
            "q": arguments["q"],
            "size": arguments.get("size", 10),
            "page": arguments.get("page", 1)
        })
        return [{"type": "text", "text": str(data)}]

    elif name == "get_person":
        data = get_json(f"/person/{arguments['id']}")
        return [{"type": "text", "text": str(data)}]

    elif name == "random_object":
        data = get_json("/object", {
            "size": 1,
            "random": 1,
            "classification": arguments.get("classification"),
            "culture": arguments.get("culture"),
            "hasimage": 1
        })
        result = data["records"][0] if data.get("records") else {}
        return [{"type": "text", "text": str(result)}]

    else:
        raise ValueError(f"Unknown tool: {name}")

# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    print("[HMA MCP] Server ready. Tools: search_objects, get_object, search_people, get_person, random_object")
    asyncio.run(main())
