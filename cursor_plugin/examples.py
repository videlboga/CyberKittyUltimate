#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Примеры использования Voice Avatar MCP Plugin в Cursor.

Для запуска необходимо сначала установить плагин и запустить MCP-сервер.
"""

import asyncio
from cursor_plugin.voice_avatar_plugin import (
    speak_text, echo_message, browse_website,
    speak_text_sync, echo_message_sync, browse_website_sync,
    VoiceAvatarPlugin
)

async def async_examples():
    """
    Примеры асинхронного использования.
    """
    # Получение информации о доступных инструментах
    print("Получение информации о доступных инструментах:")
    tools_info = await VoiceAvatarPlugin.get_tools_info()
    print(f"Доступные инструменты: {tools_info}")
    print("\n" + "-"*50 + "\n")
    
    # Пример echo_message
    print("Тестирование echo_message:")
    echo_result = await echo_message("Привет из Cursor!")
    print(f"Результат: {echo_result}")
    print("\n" + "-"*50 + "\n")
    
    # Пример speak_text
    print("Тестирование speak_text:")
    speak_result = await speak_text("Привет, это тестовое сообщение из Cursor!")
    print(f"Результат: {speak_result}")
    print("\n" + "-"*50 + "\n")
    
    # Пример browse_website
    print("Тестирование browse_website:")
    browse_result = await browse_website(
        "https://example.com", 
        "собрать основную информацию со страницы"
    )
    print(f"Результат: {browse_result}")

def sync_examples():
    """
    Примеры синхронного использования.
    """
    # Пример echo_message_sync
    print("Тестирование echo_message_sync:")
    echo_result = echo_message_sync("Привет из Cursor (синхронно)!")
    print(f"Результат: {echo_result}")
    print("\n" + "-"*50 + "\n")
    
    # Пример speak_text_sync
    print("Тестирование speak_text_sync:")
    speak_result = speak_text_sync("Привет, это синхронное сообщение из Cursor!")
    print(f"Результат: {speak_result}")
    print("\n" + "-"*50 + "\n")
    
    # Пример browse_website_sync
    print("Тестирование browse_website_sync:")
    browse_result = browse_website_sync(
        "https://example.com", 
        "собрать контактную информацию"
    )
    print(f"Результат: {browse_result}")

if __name__ == "__main__":
    print("=" * 50)
    print("АСИНХРОННЫЕ ПРИМЕРЫ")
    print("=" * 50)
    asyncio.run(async_examples())
    
    print("\n\n")
    print("=" * 50)
    print("СИНХРОННЫЕ ПРИМЕРЫ")
    print("=" * 50)
    sync_examples() 