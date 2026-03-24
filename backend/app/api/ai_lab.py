from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, AsyncGenerator
import httpx
import json
import asyncio
import logging
import time
import os

from app.core.config import settings

router = APIRouter()

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 确保有处理器
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(handler)

class PromptRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000
    stream: bool = False

class PromptResponse(BaseModel):
    output: str
    model: str
    tokens_used: int
    processing_time: float

class PromptTemplate(BaseModel):
    id: str
    name: str
    description: str
    prompt: str
    category: str


def get_model_config():
    """动态获取模型配置（支持热加载环境变量）"""
    return {
        "gpt-3.5-turbo": {
            "provider": "openai",
            "name": "GPT-3.5 Turbo",
            "api_base": settings.OPENAI_API_BASE,
            "api_key": settings.OPENAI_API_KEY,
        },
        "gpt-4": {
            "provider": "openai",
            "name": "GPT-4",
            "api_base": settings.OPENAI_API_BASE,
            "api_key": settings.OPENAI_API_KEY,
        },
        "gpt-4-turbo": {
            "provider": "openai",
            "name": "GPT-4 Turbo",
            "api_base": settings.OPENAI_API_BASE,
            "api_key": settings.OPENAI_API_KEY,
        },
        "claude-3-haiku": {
            "provider": "anthropic",
            "name": "Claude 3 Haiku",
            "api_base": settings.ANTHROPIC_API_BASE,
            "api_key": settings.ANTHROPIC_API_KEY,
        },
        "claude-3-sonnet": {
            "provider": "anthropic",
            "name": "Claude 3 Sonnet",
            "api_base": settings.ANTHROPIC_API_BASE,
            "api_key": settings.ANTHROPIC_API_KEY,
        },
        "claude-3-opus": {
            "provider": "anthropic",
            "name": "Claude 3 Opus",
            "api_base": settings.ANTHROPIC_API_BASE,
            "api_key": settings.ANTHROPIC_API_KEY,
        },
        "moonshot-v1-8k": {
            "provider": "moonshot",
            "name": "Kimi (8K)",
            "api_base": settings.MOONSHOT_API_BASE,
            "api_key": settings.MOONSHOT_API_KEY,
        },
        "moonshot-v1-32k": {
            "provider": "moonshot",
            "name": "Kimi (32K)",
            "api_base": settings.MOONSHOT_API_BASE,
            "api_key": settings.MOONSHOT_API_KEY,
        },
        "moonshot-v1-128k": {
            "provider": "moonshot",
            "name": "Kimi (128K)",
            "api_base": settings.MOONSHOT_API_BASE,
            "api_key": settings.MOONSHOT_API_KEY,
        },
        "qwen-turbo": {
            "provider": "dashscope",
            "name": "通义千问 Turbo",
            "api_base": settings.DASHSCOPE_API_BASE,
            "api_key": settings.DASHSCOPE_API_KEY,
        },
        "qwen-plus": {
            "provider": "dashscope",
            "name": "通义千问 Plus",
            "api_base": settings.DASHSCOPE_API_BASE,
            "api_key": settings.DASHSCOPE_API_KEY,
        },
        "qwen-max": {
            "provider": "dashscope",
            "name": "通义千问 Max",
            "api_base": settings.DASHSCOPE_API_BASE,
            "api_key": settings.DASHSCOPE_API_KEY,
        },
        "doubao-lite": {
            "provider": "doubao",
            "name": "豆包 Lite",
            "api_base": settings.DOUBAO_API_BASE,
            "api_key": settings.DOUBAO_API_KEY,
        },
        "doubao-pro": {
            "provider": "doubao",
            "name": "豆包 Pro",
            "api_base": settings.DOUBAO_API_BASE,
            "api_key": settings.DOUBAO_API_KEY,
        },
    }


# 预设模板
TEMPLATES = [
    {
        "id": "rewrite",
        "name": "文案改写",
        "description": "将文案改写成更专业的版本",
        "category": "写作",
        "prompt": "请改写以下文案，使其更专业、更有吸引力：\n\n{content}"
    },
    {
        "id": "email",
        "name": "邮件生成",
        "description": "生成正式商务邮件",
        "category": "办公",
        "prompt": "请帮我写一封正式的商务邮件。\n主题：{subject}\n收件人：{recipient}\n目的：{purpose}\n语气：专业礼貌"
    },
    {
        "id": "summary",
        "name": "内容摘要",
        "description": "总结长文本的核心要点",
        "category": "效率",
        "prompt": "请总结以下内容的要点，列出3-5个关键点：\n\n{content}"
    },
    {
        "id": "brainstorm",
        "name": "头脑风暴",
        "description": "围绕主题生成创意点子",
        "category": "创意",
        "prompt": "请围绕\"{topic}\"进行头脑风暴，给出10个有创意的点子。要求实用且可执行。"
    },
    {
        "id": "code-review",
        "name": "代码审查",
        "description": "检查代码并提供改进建议",
        "category": "编程",
        "prompt": "请审查以下代码，指出潜在问题并提供改进建议：\n\n```{language}\n{code}\n```"
    },
    {
        "id": "translate",
        "name": "中英翻译",
        "description": "专业中英互译",
        "category": "语言",
        "prompt": "请将以下内容翻译成{target_lang}，保持专业性和准确性：\n\n{content}"
    },
    {
        "id": "sql",
        "name": "SQL生成",
        "description": "根据描述生成SQL查询",
        "category": "编程",
        "prompt": "请根据以下需求生成SQL查询语句：\n需求：{requirement}\n表结构：{schema}"
    },
    {
        "id": "explain",
        "name": "概念解释",
        "description": "用简单语言解释复杂概念",
        "category": "学习",
        "prompt": "请用简单易懂的语言解释\"{concept}\"，适合初学者理解。包含定义、例子和应用场景。"
    }
]


async def stream_openai(response: httpx.Response) -> AsyncGenerator[str, None]:
    """解析 OpenAI 流式响应"""
    logger.debug("[流式解析] 开始解析 OpenAI 响应")
    chunk_count = 0
    async for line in response.aiter_lines():
        if line.startswith("data: "):
            data = line[6:]
            if data == "[DONE]":
                logger.debug(f"[流式解析] 收到 [DONE]，共 {chunk_count} 个 chunk")
                break
            try:
                json_data = json.loads(data)
                if "choices" in json_data and len(json_data["choices"]) > 0:
                    delta = json_data["choices"][0].get("delta", {})
                    if "content" in delta:
                        chunk_count += 1
                        yield delta["content"]
            except json.JSONDecodeError:
                continue
    logger.debug(f"[流式解析] 结束，总 chunk 数: {chunk_count}")


async def stream_anthropic(response: httpx.Response) -> AsyncGenerator[str, None]:
    """解析 Anthropic 流式响应"""
    logger.debug("[流式解析] 开始解析 Anthropic 响应")
    chunk_count = 0
    async for line in response.aiter_lines():
        if line.startswith("data: "):
            data = line[6:]
            try:
                json_data = json.loads(data)
                if json_data.get("type") == "content_block_delta":
                    delta = json_data.get("delta", {})
                    if "text" in delta:
                        chunk_count += 1
                        yield delta["text"]
            except json.JSONDecodeError:
                continue
    logger.debug(f"[流式解析] 结束，总 chunk 数: {chunk_count}")


async def call_openai(
    prompt: str,
    model: str,
    config: dict,
    temperature: float,
    max_tokens: int,
    stream: bool = False
) -> AsyncGenerator[str, None]:
    """调用 OpenAI API"""
    logger.info(f"[OpenAI调用] 开始 - 模型={model}, 流式={stream}")
    
    if not config["api_key"]:
        logger.error("[OpenAI调用] API Key 未配置")
        raise HTTPException(status_code=500, detail="OpenAI API Key 未配置")
    
    url = f"{config['api_base']}/chat/completions"
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
    }
    
    logger.debug(f"[OpenAI调用] URL={url}, 模型={model}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
                timeout=120.0,
            )
            
            logger.info(f"[OpenAI调用] HTTP状态码: {response.status_code}")
            
            if response.status_code != 200:
                error_text = await response.aread()
                logger.error(f"[OpenAI调用] 错误响应: {error_text}")
                raise HTTPException(status_code=response.status_code, 
                                  detail=f"OpenAI API 错误: {error_text}")
            
            if stream:
                logger.info("[OpenAI调用] 开始流式响应")
                async for chunk in stream_openai(response):
                    yield chunk
            else:
                result = response.json()
                logger.debug(f"[OpenAI调用] 响应: {result}")
                if "choices" in result:
                    yield result["choices"][0]["message"]["content"]
                else:
                    raise HTTPException(status_code=500, detail=f"OpenAI API 错误: {result}")
    except httpx.TimeoutException:
        logger.error("[OpenAI调用] 请求超时")
        raise HTTPException(status_code=504, detail="OpenAI API 请求超时")
    except Exception as e:
        logger.error(f"[OpenAI调用] 异常: {str(e)}")
        raise


async def call_anthropic(
    prompt: str,
    model: str,
    config: dict,
    temperature: float,
    max_tokens: int,
    stream: bool = False
) -> AsyncGenerator[str, None]:
    """调用 Anthropic Claude API"""
    logger.info(f"[Claude调用] 开始 - 模型={model}, 流式={stream}")
    
    if not config["api_key"]:
        logger.error("[Claude调用] API Key 未配置")
        raise HTTPException(status_code=500, detail="Anthropic API Key 未配置")
    
    model_map = {
        "claude-3-haiku": "claude-3-haiku-20240307",
        "claude-3-sonnet": "claude-3-sonnet-20240229",
        "claude-3-opus": "claude-3-opus-20240229",
    }
    anthropic_model = model_map.get(model, model)
    
    url = f"{config['api_base']}/v1/messages"
    headers = {
        "x-api-key": config["api_key"],
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    payload = {
        "model": anthropic_model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": stream,
    }
    
    logger.debug(f"[Claude调用] URL={url}, 模型={anthropic_model}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
                timeout=120.0,
            )
            
            logger.info(f"[Claude调用] HTTP状态码: {response.status_code}")
            
            if response.status_code != 200:
                error_text = await response.aread()
                logger.error(f"[Claude调用] 错误响应: {error_text}")
                raise HTTPException(status_code=response.status_code,
                                  detail=f"Anthropic API 错误: {error_text}")
            
            if stream:
                logger.info("[Claude调用] 开始流式响应")
                async for chunk in stream_anthropic(response):
                    yield chunk
            else:
                result = response.json()
                logger.debug(f"[Claude调用] 响应: {result}")
                if "content" in result:
                    yield result["content"][0]["text"]
                else:
                    raise HTTPException(status_code=500, detail=f"Anthropic API 错误: {result}")
    except httpx.TimeoutException:
        logger.error("[Claude调用] 请求超时")
        raise HTTPException(status_code=504, detail="Anthropic API 请求超时")
    except Exception as e:
        logger.error(f"[Claude调用] 异常: {str(e)}")
        raise


async def call_moonshot(
    prompt: str,
    model: str,
    config: dict,
    temperature: float,
    max_tokens: int,
    stream: bool = False
) -> AsyncGenerator[str, None]:
    """调用 Moonshot (Kimi) API"""
    logger.info(f"[Moonshot调用] 开始 - 模型={model}, 流式={stream}")
    
    if not config["api_key"]:
        logger.error("[Moonshot调用] API Key 未配置")
        raise HTTPException(status_code=500, detail="Moonshot API Key 未配置")
    
    url = f"{config['api_base']}/chat/completions"
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
    }
    
    logger.debug(f"[Moonshot调用] URL={url}, 模型={model}")
    logger.debug(f"[Moonshot调用] API Key 前10位: {config['api_key'][:10]}...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
                timeout=120.0,
            )
            
            logger.info(f"[Moonshot调用] HTTP状态码: {response.status_code}")
            
            if response.status_code != 200:
                error_text = await response.aread()
                logger.error(f"[Moonshot调用] 错误响应: {error_text}")
                raise HTTPException(status_code=response.status_code,
                                  detail=f"Moonshot API 错误: {error_text}")
            
            if stream:
                logger.info("[Moonshot调用] 开始流式响应")
                async for chunk in stream_openai(response):
                    yield chunk
            else:
                result = response.json()
                logger.debug(f"[Moonshot调用] 响应: {result}")
                if "choices" in result:
                    yield result["choices"][0]["message"]["content"]
                else:
                    raise HTTPException(status_code=500, detail=f"Moonshot API 错误: {result}")
    except httpx.TimeoutException:
        logger.error("[Moonshot调用] 请求超时")
        raise HTTPException(status_code=504, detail="Moonshot API 请求超时")
    except Exception as e:
        logger.error(f"[Moonshot调用] 异常: {str(e)}")
        raise


async def call_dashscope(
    prompt: str,
    model: str,
    config: dict,
    temperature: float,
    max_tokens: int,
    stream: bool = False
) -> AsyncGenerator[str, None]:
    """调用 DashScope (通义千问) API"""
    logger.info(f"[DashScope调用] 开始 - 模型={model}")
    
    if not config["api_key"]:
        logger.error("[DashScope调用] API Key 未配置")
        raise HTTPException(status_code=500, detail="DashScope API Key 未配置")
    
    model_map = {
        "qwen-turbo": "qwen-turbo",
        "qwen-plus": "qwen-plus",
        "qwen-max": "qwen-max",
    }
    qwen_model = model_map.get(model, model)
    
    url = f"{config['api_base']}/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": qwen_model,
        "input": {"messages": [{"role": "user", "content": prompt}]},
        "parameters": {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "result_format": "message",
        },
    }
    
    logger.debug(f"[DashScope调用] URL={url}, 模型={qwen_model}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
                timeout=120.0,
            )
            
            logger.info(f"[DashScope调用] HTTP状态码: {response.status_code}")
            
            if response.status_code != 200:
                error_text = await response.aread()
                logger.error(f"[DashScope调用] 错误响应: {error_text}")
                raise HTTPException(status_code=response.status_code,
                                  detail=f"DashScope API 错误: {error_text}")
            
            result = response.json()
            logger.debug(f"[DashScope调用] 响应: {result}")
            
            if "output" in result and "choices" in result["output"]:
                yield result["output"]["choices"][0]["message"]["content"]
            else:
                raise HTTPException(status_code=500, detail=f"DashScope API 错误: {result}")
    except httpx.TimeoutException:
        logger.error("[DashScope调用] 请求超时")
        raise HTTPException(status_code=504, detail="DashScope API 请求超时")
    except Exception as e:
        logger.error(f"[DashScope调用] 异常: {str(e)}")
        raise


async def call_doubao(
    prompt: str,
    model: str,
    config: dict,
    temperature: float,
    max_tokens: int,
    stream: bool = False
) -> AsyncGenerator[str, None]:
    """调用豆包 API"""
    logger.info(f"[Doubao调用] 开始 - 模型={model}")
    
    if not config["api_key"]:
        logger.error("[Doubao调用] API Key 未配置")
        raise HTTPException(status_code=500, detail="豆包 API Key 未配置")
    
    model_map = {
        "doubao-lite": "doubao-lite-4k",
        "doubao-pro": "doubao-pro-4k",
    }
    doubao_model = model_map.get(model, model)
    
    url = f"{config['api_base']}/chat/completions"
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": doubao_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    logger.debug(f"[Doubao调用] URL={url}, 模型={doubao_model}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
                timeout=120.0,
            )
            
            logger.info(f"[Doubao调用] HTTP状态码: {response.status_code}")
            
            if response.status_code != 200:
                error_text = await response.aread()
                logger.error(f"[Doubao调用] 错误响应: {error_text}")
                raise HTTPException(status_code=response.status_code,
                                  detail=f"豆包 API 错误: {error_text}")
            
            result = response.json()
            logger.debug(f"[Doubao调用] 响应: {result}")
            
            if "choices" in result:
                yield result["choices"][0]["message"]["content"]
            else:
                raise HTTPException(status_code=500, detail=f"豆包 API 错误: {result}")
    except httpx.TimeoutException:
        logger.error("[Doubao调用] 请求超时")
        raise HTTPException(status_code=504, detail="豆包 API 请求超时")
    except Exception as e:
        logger.error(f"[Doubao调用] 异常: {str(e)}")
        raise


async def call_ai_model(
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
    stream: bool = False
) -> AsyncGenerator[str, None]:
    """统一调用入口"""
    MODEL_CONFIG = get_model_config()
    
    if model not in MODEL_CONFIG:
        raise HTTPException(status_code=400, detail=f"不支持的模型: {model}")
    
    config = MODEL_CONFIG[model]
    provider = config["provider"]
    
    # 记录调用日志
    has_key = bool(config.get("api_key"))
    logger.info(f"[AI调用] 模型={model}, 提供商={provider}, 流式={stream}, Key配置={has_key}")
    
    if provider == "openai":
        async for chunk in call_openai(prompt, model, config, temperature, max_tokens, stream):
            yield chunk
    elif provider == "anthropic":
        async for chunk in call_anthropic(prompt, model, config, temperature, max_tokens, stream):
            yield chunk
    elif provider == "moonshot":
        async for chunk in call_moonshot(prompt, model, config, temperature, max_tokens, stream):
            yield chunk
    elif provider == "dashscope":
        async for chunk in call_dashscope(prompt, model, config, temperature, max_tokens, stream):
            yield chunk
    elif provider == "doubao":
        async for chunk in call_doubao(prompt, model, config, temperature, max_tokens, stream):
            yield chunk
    else:
        raise HTTPException(status_code=400, detail=f"不支持的提供商: {provider}")


@router.post("/chat")
async def chat_with_ai(request: PromptRequest):
    """
    与AI模型对话（支持流式和非流式）
    """
    MODEL_CONFIG = get_model_config()
    
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="提示词不能为空")
    
    # 检查模型配置
    if request.model not in MODEL_CONFIG:
        logger.warning(f"[AI调用] 无效模型: {request.model}")
        raise HTTPException(status_code=400, detail=f"不支持的模型: {request.model}")
    
    config = MODEL_CONFIG[request.model]
    has_key = bool(config.get("api_key"))
    
    if not has_key:
        logger.error(f"[AI调用] 模型 {request.model} 未配置API Key")
        raise HTTPException(status_code=500, detail=f"模型 {request.model} 未配置API Key，请在.env中配置 {request.model.upper().replace('-', '_')}_API_KEY")
    
    logger.info(f"[AI调用] 开始 - 模型={request.model}, 流式={request.stream}, 提示词长度={len(request.prompt)}")
    
    if request.stream:
        # 流式响应
        async def event_generator():
            start_time = time.time()
            total_chars = 0
            try:
                async for chunk in call_ai_model(
                    request.prompt,
                    request.model,
                    request.temperature,
                    request.max_tokens,
                    stream=True
                ):
                    total_chars += len(chunk)
                    yield f"data: {json.dumps({'content': chunk})}\n\n"
                
                elapsed = time.time() - start_time
                logger.info(f"[AI调用] 完成 - 模型={request.model}, 耗时={elapsed:.2f}s, 输出长度={total_chars}")
                yield "data: [DONE]\n\n"
            except Exception as e:
                logger.error(f"[AI调用] 错误 - 模型={request.model}, 错误={str(e)}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )
    else:
        # 非流式响应
        start_time = time.time()
        
        output = ""
        try:
            async for chunk in call_ai_model(
                request.prompt,
                request.model,
                request.temperature,
                request.max_tokens,
                stream=False
            ):
                output += chunk
            
            processing_time = time.time() - start_time
            tokens_used = len(request.prompt.split()) + len(output.split())
            
            logger.info(f"[AI调用] 完成 - 模型={request.model}, 耗时={processing_time:.2f}s, tokens={tokens_used}")
            
            return PromptResponse(
                output=output,
                model=request.model,
                tokens_used=tokens_used,
                processing_time=round(processing_time, 2)
            )
        except Exception as e:
            logger.error(f"[AI调用] 错误 - 模型={request.model}, 错误={str(e)}")
            raise


@router.get("/templates", response_model=List[PromptTemplate])
async def get_templates(category: Optional[str] = None):
    """获取提示词模板列表"""
    if category:
        return [t for t in TEMPLATES if t["category"] == category]
    return TEMPLATES


@router.get("/models")
async def get_available_models():
    """获取可用的AI模型列表"""
    MODEL_CONFIG = get_model_config()
    available_models = []
    
    for model_id, config in MODEL_CONFIG.items():
        # 检查是否配置了 API Key
        has_key = bool(config["api_key"])
        
        model_info = {
            "id": model_id,
            "name": config["name"],
            "provider": config["provider"],
            "available": has_key,
        }
        
        # 添加额外信息
        if config["provider"] == "openai":
            model_info["max_tokens"] = 4096 if "3.5" in model_id else 8192
            model_info["capabilities"] = ["text", "code", "analysis"]
        elif config["provider"] == "anthropic":
            model_info["max_tokens"] = 4096 if "haiku" in model_id else 8192
            model_info["capabilities"] = ["text", "code", "analysis", "reasoning"]
        elif config["provider"] == "moonshot":
            model_info["max_tokens"] = 8192 if "8k" in model_id else (32768 if "32k" in model_id else 128000)
            model_info["capabilities"] = ["text", "code", "analysis", "long_context"]
        elif config["provider"] == "dashscope":
            model_info["max_tokens"] = 8192
            model_info["capabilities"] = ["text", "code", "analysis", "chinese"]
        elif config["provider"] == "doubao":
            model_info["max_tokens"] = 4096
            model_info["capabilities"] = ["text", "code", "analysis", "chinese"]
        
        available_models.append(model_info)
    
    return available_models


@router.get("/history")
async def get_chat_history(user_id: Optional[int] = None, limit: int = 20):
    """获取用户的对话历史"""
    return {
        "items": [],
        "total": 0
    }


# 启动时打印配置信息
logger.info("=" * 60)
logger.info("AI Lab 模块加载完成")
logger.info(f"支持的模型数量: {len(get_model_config())}")
logger.info("=" * 60)
