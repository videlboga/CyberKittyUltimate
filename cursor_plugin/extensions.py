#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Расширенные функции для интеграции Voice Avatar MCP Server с Cursor.
Этот модуль содержит функции, которые могут быть вызваны непосредственно из Cursor
для обработки выделенного текста, кода и другого контента.
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

# Импортируем функции из основного плагина
from cursor_plugin.voice_avatar_plugin import (
    speak_text_sync, 
    speak_text, 
    browse_website_sync, 
    browse_website,
    echo_message_sync,
    echo_message,
    get_tools_info_sync,
    get_tools_info
)

# Путь к директории вывода для сохранения результатов
OUTPUT_DIR = Path("/home/cyberkitty/my_mcp/output")
OUTPUT_DIR.mkdir(exist_ok=True)

def process_selected_text(text: str, action: str = "speak") -> Dict[str, Any]:
    """
    Обрабатывает выделенный в Cursor текст.
    
    Args:
        text (str): Выделенный текст из Cursor.
        action (str): Тип действия ("speak", "browse", "explain").
        
    Returns:
        Dict[str, Any]: Результат обработки.
    """
    result = {"success": False, "message": "", "data": None}
    
    try:
        if not text:
            result["message"] = "Не выделен текст для обработки"
            return result
            
        if action == "speak":
            # Преобразуем выделенный текст в речь
            audio_path = speak_text_sync(text)
            result["success"] = True
            result["message"] = f"Текст успешно преобразован в речь"
            result["data"] = {"audio_path": audio_path}
            
        elif action == "browse":
            # Используем выделенный текст как запрос для браузера
            if "://" in text:
                # Если текст содержит URL, используем его как адрес
                parts = text.split(maxsplit=1)
                url = parts[0]
                task = parts[1] if len(parts) > 1 else "собрать общую информацию"
            else:
                # Иначе используем как поисковый запрос
                url = "https://www.google.com"
                task = f"найти информацию о {text}"
                
            browser_result = browse_website_sync(url, task)
            result["success"] = True
            result["message"] = f"Выполнен поиск информации"
            result["data"] = {"result": browser_result}
            
        elif action == "explain":
            # Объясняем выделенный код
            # Сначала сохраняем код во временный файл
            temp_file = OUTPUT_DIR / "temp_code.py"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(text)
                
            # Используем браузер для поиска документации
            explanation = browse_website_sync(
                "https://docs.python.org", 
                f"найти объяснение и примеры использования для этого кода: {text[:100]}..."
            )
            
            # Озвучиваем объяснение
            audio_path = speak_text_sync(explanation)
            
            result["success"] = True
            result["message"] = "Код объяснен и озвучен"
            result["data"] = {
                "explanation": explanation,
                "audio_path": audio_path
            }
        else:
            result["message"] = f"Неизвестное действие: {action}"
            
    except Exception as e:
        result["message"] = f"Ошибка при обработке текста: {str(e)}"
        
    return result

def get_cursor_selection() -> str:
    """
    Получает текущее выделение в Cursor (заглушка).
    В реальном плагине эта функция будет использовать API Cursor.
    
    Returns:
        str: Выделенный текст.
    """
    # Это заглушка. В реальном плагине здесь будет код для получения 
    # выделенного текста через API Cursor
    return os.environ.get("CURSOR_SELECTION", "")

def execute_cursor_command(command: str, args: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Выполняет команду Cursor.
    
    Args:
        command (str): Имя команды.
        args (Dict[str, Any], optional): Аргументы команды.
        
    Returns:
        Dict[str, Any]: Результат выполнения команды.
    """
    args = args or {}
    result = {"success": False, "message": "", "data": None}
    
    try:
        if command == "speak_selection":
            text = get_cursor_selection()
            return process_selected_text(text, "speak")
            
        elif command == "browse_selection":
            text = get_cursor_selection()
            return process_selected_text(text, "browse")
            
        elif command == "explain_selection":
            text = get_cursor_selection()
            return process_selected_text(text, "explain")
            
        elif command == "get_tools":
            tools = get_tools_info_sync()
            result["success"] = True
            result["message"] = "Получен список инструментов"
            result["data"] = {"tools": tools}
            
        else:
            result["message"] = f"Неизвестная команда: {command}"
            
    except Exception as e:
        result["message"] = f"Ошибка при выполнении команды: {str(e)}"
        
    return result

if __name__ == "__main__":
    # Пример использования
    # В реальном плагине, эта часть будет заменена на регистрацию команд в Cursor
    
    # Симулируем выделенный текст
    os.environ["CURSOR_SELECTION"] = "Привет! Это тестовый текст для преобразования в речь."
    
    # Выполняем команду
    result = execute_cursor_command("speak_selection")
    print(json.dumps(result, ensure_ascii=False, indent=2)) 