import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from translate import router

load_dotenv()

app = FastAPI()

app.include_router(router)

mcp = FastApiMCP(
    app,
    name="translate",
    description="MCP server for the translate",
    describe_full_response_schema=True,  # Describe the full response JSON-schema instead of just a response example
    describe_all_responses=True,  # Describe all the possible responses instead of just the success (2XX) response
)

mcp.mount()

def main():
    import uvicorn
    uvicorn.run(app, port=os.getenv("PORT", 8899))


if __name__ == "__main__":
    main()
