#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP-сервер для голосового интерфейса с анимированным персонажем.
"""

import os
import time
import subprocess
import tempfile
from typing import Annotated, Any, Dict, Optional
from fastmcp import FastMCP

# Создание директорий для выходных файлов
OUTPUT_DIR = os.path.expanduser("~/my_mcp/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Инициализация MCP-сервера
app = FastMCP(title="Voice Avatar MCP Server")

@app.tool("echo_message")
def echo_message(
    message: Annotated[str, "Сообщение для эхо-ответа"]
) -> Dict[str, str]:
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

@app.tool("speak_text")
def speak_text(
    text: Annotated[str, "Текст для преобразования в речь"],
    voice_model: Annotated[str, "Модель голоса (по умолчанию ru_RU-irina-medium)"] = "ru_RU-irina-medium"
) -> Dict[str, str]:
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
        subprocess.run(command, shell=True, check=True)
        
        return {
            "message": f"Создан аудиофайл с текстом: {text[:50]}{'...' if len(text) > 50 else ''}",
            "audio_path": output_file
        }
    except subprocess.CalledProcessError as e:
        return {
            "error": f"Ошибка при генерации речи: {str(e)}",
            "command": command
        }
    finally:
        # Удаляем временный файл
        os.unlink(temp_path)

@app.tool("browse_website")
async def browse_website(
    url: Annotated[str, "URL веб-сайта для посещения"],
    task: Annotated[str, "Задача, которую нужно выполнить на сайте"] = "собрать информацию"
) -> Dict[str, Any]:
    """
    Открывает браузер и выполняет задачу на указанном веб-сайте с использованием Browser-Use.
    """
    from browser_use import Agent
    from langchain_openai import ChatOpenAI
    import asyncio
    import json
    
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

if __name__ == "__main__":
    # Запускаем сервер напрямую с помощью методов FastMCP
    # FastMCP автоматически запустит Uvicorn сервер
    port = 8000
    host = "127.0.0.1"
    print(f"Запуск MCP-сервера на http://{host}:{port}")
    app.run(host=host, port=port) 