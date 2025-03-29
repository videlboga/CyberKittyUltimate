#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP-сервер для голосового интерфейса с анимированным персонажем.
Использует Starlette для создания веб-сервера.
"""

import os
import time
import subprocess
import tempfile
import json
import asyncio
from typing import Annotated, Any, Dict, Optional, List
from pydantic import BaseModel, Field
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request

# Создание директорий для выходных файлов
OUTPUT_DIR = os.path.expanduser("~/my_mcp/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Модель для инструментов
class ToolCall(BaseModel):
    name: str
    parameters: Dict[str, Any]

# Инструменты MCP
async def echo_message(message: str) -> Dict[str, str]:
    """
    Простой тестовый инструмент, возвращающий переданное сообщение.
    """
    timestamp = int(time.time())
    output_file = f"{OUTPUT_DIR}/echo_{timestamp}.txt"
    
    # Запись сообщения в файл
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(message)
    
    return {
        "message": f"Получено сообщение: {message}",
        "output_file": output_file
    }

async def speak_text(text: str, voice_model: str = "ru_RU-irina-medium") -> Dict[str, str]:
    """
    Преобразует текст в речь с помощью Piper TTS.
    """
    timestamp = int(time.time())
    output_file = f"{OUTPUT_DIR}/speech_{timestamp}.wav"
    
    # Создаем временный файл для текста
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp:
        temp.write(text)
        temp_path = temp.name
    
    try:
        # Используем Piper для генерации речи
        command = f'cat {temp_path} | piper --model {voice_model} --output_file {output_file}'
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            return {
                "error": f"Ошибка при генерации речи: {stderr.decode()}",
                "command": command
            }
        
        return {
            "message": f"Создан аудиофайл с текстом: {text[:50]}{'...' if len(text) > 50 else ''}",
            "audio_path": output_file
        }
    except Exception as e:
        return {
            "error": f"Ошибка при генерации речи: {str(e)}",
            "command": command
        }
    finally:
        # Удаляем временный файл
        os.unlink(temp_path)

async def browse_website(url: str, task: str = "собрать информацию") -> Dict[str, Any]:
    """
    Открывает браузер и выполняет задачу на указанном веб-сайте с использованием Browser-Use.
    """
    from browser_use import Agent
    from langchain_openai import ChatOpenAI
    
    try:
        # Создание агента Browser-Use
        agent = Agent(
            task=f"Посетить сайт {url} и {task}. Сохранить результаты в файл.",
            llm=ChatOpenAI(model="gpt-4o"),
        )
        
        # Выполнение задачи
        result = await agent.run()
        
        # Сохранение результатов
        timestamp = int(time.time())
        output_file = f"{OUTPUT_DIR}/browser_task_{timestamp}.json"
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return {
            "message": f"Браузер выполнил задачу на {url}",
            "task": task,
            "output_file": output_file,
            "result": result
        }
    except Exception as e:
        return {
            "error": f"Ошибка при работе с браузером: {str(e)}",
            "url": url,
            "task": task
        }

# Маршрутизация инструментов
TOOLS = {
    "echo_message": echo_message,
    "speak_text": speak_text,
    "browse_website": browse_website,
}

async def tool_handler(request: Request):
    """
    Обработчик запросов к инструментам MCP
    """
    try:
        data = await request.json()
        tool_name = data.get("name")
        parameters = data.get("parameters", {})
        
        if tool_name not in TOOLS:
            return JSONResponse(
                {"error": f"Инструмент '{tool_name}' не найден"},
                status_code=404
            )
        
        result = await TOOLS[tool_name](**parameters)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )

async def mcp_tools_info(request: Request):
    """
    Возвращает информацию о доступных инструментах
    """
    tools_info = []
    for name, func in TOOLS.items():
        tools_info.append({
            "name": name,
            "description": func.__doc__.strip() if func.__doc__ else "Нет описания"
        })
    
    return JSONResponse({
        "title": "Voice Avatar MCP Server",
        "tools": tools_info
    })

# Создание Starlette приложения
routes = [
    Route("/mcp/tools", endpoint=tool_handler, methods=["POST"]),
    Route("/mcp/info", endpoint=mcp_tools_info, methods=["GET"]),
]

app = Starlette(
    debug=True, 
    routes=routes
)

if __name__ == "__main__":
    import uvicorn
    
    host = "127.0.0.1"
    port = 8000
    print(f"Запуск MCP-сервера на http://{host}:{port}")
    uvicorn.run(app, host=host, port=port) 