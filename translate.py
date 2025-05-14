import base64
import os
from typing import Optional

from fastapi import APIRouter
from litellm import aspeech as litellm_tts, acompletion
from pydantic import BaseModel, Field

router = APIRouter(tags=["translate"])


class TranslateRequest(BaseModel):
    text: str = Field(..., description="need to be translated text")
    source_language: str = Field(..., description="source language code, e.g. 'en', 'zh', 'es'")
    target_language: str = Field(..., description="target language code, e.g. 'en', 'zh', 'es'")
    convert_to_speech: bool = Field(False, description="whether to convert source text to speech")
    voice: str = Field("alloy", description="voice to use for speech (alloy, echo, fable, onyx, nova, shimmer)")


class TranslateResponse(BaseModel):
    translated_text: str = Field(..., description="translated text in target language")
    success: bool = Field(..., description="whether translation was successful")
    error: Optional[str] = Field(None, description="error message if translation failed")
    type: str = Field(..., description="type of response, e.g. 'text', 'audio'")
    content: Optional[str] = Field(None, description="base64 encoded audio of source text (if requested)")


async def text_to_speech(text: str, voice: str = "alloy") -> Optional[str]:
    """
    使用litellm调用OpenAI的TTS API转换文本为语音，返回Base64编码的音频数据

    Args:
        text: 要转换的文本
        voice: 要使用的声音 (alloy, echo, fable, onyx, nova, shimmer)

    Returns:
        Base64编码的MP3音频数据
    """
    try:
        # 使用litellm调用TTS API
        audio_response = await litellm_tts(
            model=os.getenv("VOICE_MODEL"),
            input=text,
            voice=voice,
            api_key=os.getenv("VOICE_API_KEY")
        )

        # 获取音频内容并转换为Base64
        audio_data = audio_response.content
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        return audio_base64
    except Exception as e:
        print(f"Error converting text to speech: {str(e)}")
        return None


async def get_translate_voice(request: TranslateRequest, translated_text: str) -> Optional[str]:
    if not request.convert_to_speech:
        return None

    mother_language = os.getenv("MOTHER_LANGUAGE", 'zh')
    if mother_language == request.source_language:
        return await text_to_speech(translated_text, request.voice)
    return await text_to_speech(request.text, request.voice)


@router.post("/api/translate", response_model=TranslateResponse, operation_id="translate")
async def translate(request: TranslateRequest) -> TranslateResponse:
    try:
        prompt = f"""Please translate the following text from {request.source_language} to {request.target_language}.
Only return the translated text, do not add any explanation or extra content.

source text: {request.text}

translated text:"""

        response = await acompletion(
            model=os.getenv("MODEL"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,  # lower temperature for more accurate translation
            api_key=os.getenv("API_KEY"),
            api_base=os.getenv("API_BASE")
        )

        # 提取生成的翻译文本
        translated_text = response.choices[0].message.content.strip()
        audio_base64 =  await get_translate_voice(request, translated_text)
        return TranslateResponse(
            translated_text=translated_text,
            success=True,
            error=None,
            content=audio_base64,
            type="text" if audio_base64 is None else "audio"
        )
    except Exception as e:
        error_message = f"translation error: {str(e)}"
        return TranslateResponse(
            translated_text="",
            success=False,
            error=error_message,
            type="text",
            content=None
        )
