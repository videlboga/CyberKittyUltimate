#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестирование плагина Voice Avatar MCP Plugin
"""

import sys
import os

# Добавляем директорию проекта в путь Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from cursor_plugin.voice_avatar_plugin import echo_message_sync
    
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ ПЛАГИНА CURSOR")
    print("=" * 50)
    
    # Отправляем тестовое сообщение
    message = "Привет! Это тест интеграции Cursor с MCP-сервером."
    print(f"Отправка сообщения: {message}")
    
    result = echo_message_sync(message)
    
    print("\nРезультат:")
    print(f"- Сообщение: {result.get('message', 'Нет сообщения')}")
    print(f"- Выходной файл: {result.get('output_file', 'Нет файла')}")
    
    # Проверяем наличие файла
    if 'output_file' in result and os.path.exists(result['output_file']):
        print(f"\nСодержимое файла {result['output_file']}:")
        with open(result['output_file'], 'r', encoding='utf-8') as f:
            print(f.read())
    
    print("\nТест завершен успешно!")
    
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что плагин установлен и директория проекта добавлена в PYTHONPATH")
    sys.exit(1)
except Exception as e:
    print(f"Ошибка при тестировании: {e}")
    sys.exit(1) 