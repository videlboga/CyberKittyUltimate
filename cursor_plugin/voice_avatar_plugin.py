#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Плагин для Cursor, обеспечивающий взаимодействие с Voice Avatar MCP сервером.
"""

import os
import json
import asyncio
import httpx
from typing import Dict, Any, Optional, List, Union

# Настройки подключения к MCP-серверу
MCP_SERVER_URL = "http://127.0.0.1:8000"
MCP_TOOLS_URL = f"{MCP_SERVER_URL}/mcp/tools"
MCP_INFO_URL = f"{MCP_SERVER_URL}/mcp/info"

class VoiceAvatarPlugin:
    """
    Класс плагина для интеграции с Voice Avatar MCP сервером.
    """
    
    @staticmethod
    async def get_tools_info() -> Dict[str, Any]:
        """
        Получает информацию о доступных инструментах MCP-сервера.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(MCP_INFO_URL)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Ошибка получения информации: {response.status_code} - {response.text}")
    
    @staticmethod
    async def call_tool(tool_name: str, **parameters) -> Dict[str, Any]:
        """
        Вызывает инструмент MCP-сервера с указанными параметрами.
        """
        payload = {
            "name": tool_name,
            "parameters": parameters
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(MCP_TOOLS_URL, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Ошибка вызова инструмента: {response.status_code} - {response.text}")
    
    @staticmethod
    async def speak_text(text: str, voice_model: str = "ru_RU-irina-medium") -> Dict[str, Any]:
        """
        Преобразует текст в речь.
        """
        return await VoiceAvatarPlugin.call_tool("speak_text", text=text, voice_model=voice_model)
    
    @staticmethod
    async def echo_message(message: str) -> Dict[str, Any]:
        """
        Отправляет тестовое сообщение.
        """
        return await VoiceAvatarPlugin.call_tool("echo_message", message=message)
    
    @staticmethod
    async def browse_website(url: str, task: str = "собрать информацию") -> Dict[str, Any]:
        """
        Автоматизирует работу с браузером.
        """
        return await VoiceAvatarPlugin.call_tool("browse_website", url=url, task=task)

# Функции для использования в Cursor

async def speak_text(text: str, voice_model: str = "ru_RU-irina-medium") -> Dict[str, Any]:
    """
    Функция для преобразования текста в речь из Cursor.
    
    Пример использования:
    ```python
    await speak_text("Привет, мир!")
    ```
    """
    return await VoiceAvatarPlugin.speak_text(text, voice_model)

async def echo_message(message: str) -> Dict[str, Any]:
    """
    Функция для отправки тестового сообщения из Cursor.
    
    Пример использования:
    ```python
    await echo_message("Тестовое сообщение")
    ```
    """
    return await VoiceAvatarPlugin.echo_message(message)

async def browse_website(url: str, task: str = "собрать информацию") -> Dict[str, Any]:
    """
    Функция для автоматизации работы с браузером из Cursor.
    
    Пример использования:
    ```python
    await browse_website("https://example.com", "найти контактную информацию")
    ```
    """
    return await VoiceAvatarPlugin.browse_website(url, task)

# Синхронные обертки для удобства использования в Cursor
def speak_text_sync(text: str, voice_model: str = "ru_RU-irina-medium") -> Dict[str, Any]:
    """
    Синхронная функция для преобразования текста в речь из Cursor.
    """
    return asyncio.run(speak_text(text, voice_model))

def echo_message_sync(message: str) -> Dict[str, Any]:
    """
    Синхронная функция для отправки тестового сообщения из Cursor.
    """
    return asyncio.run(echo_message(message))

def browse_website_sync(url: str, task: str = "собрать информацию") -> Dict[str, Any]:
    """
    Синхронная функция для автоматизации работы с браузером из Cursor.
    """
    return asyncio.run(browse_website(url, task))

# Регистрация команд плагина в Cursor
commands = {
    "speak_text": speak_text_sync,
    "echo_message": echo_message_sync,
    "browse_website": browse_website_sync,
    "get_tools_info": lambda: asyncio.run(VoiceAvatarPlugin.get_tools_info())
} 