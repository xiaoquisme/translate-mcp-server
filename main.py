import os
from litellm import completion, _turn_on_debug
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional

from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

load_dotenv()

app = FastAPI()

mcp = FastApiMCP(app)

_turn_on_debug()

mcp = FastApiMCP(
    app,
    name="translate",
    description="MCP server for the translate",
    describe_full_response_schema=True,  # Describe the full response JSON-schema instead of just a response example
    describe_all_responses=True,  # Describe all the possible responses instead of just the success (2XX) response
)

mcp.mount()

class TranslateRequest(BaseModel):
    text: str = Field(..., description="need to be translated text")
    source_language: str = Field(..., description="source language code, e.g. 'en', 'zh', 'es'")
    target_language: str = Field(..., description="target language code, e.g. 'en', 'zh', 'es'")

class TranslateResponse(BaseModel):
    translated_text: str = Field(..., description="translated text in target language")
    success: bool = Field(..., description="whether translation was successful")
    error: Optional[str] = Field(None, description="error message if translation failed")


@app.post("/api/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest) -> TranslateResponse:
    try:
        prompt = f"""Please translate the following text from {request.source_language} to {request.target_language}.
Only return the translated text, do not add any explanation or extra content.

source text: {request.text}

translated text:"""

        response = completion(
            model=os.getenv("MODEL"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,  # lower temperature for more accurate translation
            api_key=os.getenv("API_KEY"),
            api_base=os.getenv("API_BASE")
        )
        
        # 提取生成的翻译文本
        translated_text = response.choices[0].message.content.strip()
        return TranslateResponse(
            translated_text=translated_text,
            success=True,
            error=None
        )
    except Exception as e:
        error_message = f"translation error: {str(e)}"
        return TranslateResponse(
            translated_text="",
            success=False,
            error=error_message
        )

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", 9988))

if __name__ == "__main__":
    main()


