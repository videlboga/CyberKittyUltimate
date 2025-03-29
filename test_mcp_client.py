#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестовый клиент для MCP-сервера.
"""

import requests
import json
import time
import argparse
import sys

MCP_API_URL = "http://localhost:8000/mcp/tools"

def call_echo_message(message):
    """
    Тестирование функции echo_message.
    """
    payload = {
        "name": "echo_message",
        "parameters": {
            "message": message
        }
    }
    
    response = requests.post(MCP_API_URL, json=payload)
    return response.json()

def call_speak_text(text, voice_model="ru_RU-irina-medium"):
    """
    Тестирование функции speak_text.
    """
    payload = {
        "name": "speak_text",
        "parameters": {
            "text": text,
            "voice_model": voice_model
        }
    }
    
    response = requests.post(MCP_API_URL, json=payload)
    return response.json()

def call_browse_website(url, task="собрать информацию"):
    """
    Тестирование функции browse_website.
    """
    payload = {
        "name": "browse_website",
        "parameters": {
            "url": url,
            "task": task
        }
    }
    
    response = requests.post(MCP_API_URL, json=payload)
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="MCP Client для тестирования")
    parser.add_argument("--echo", help="Эхо-тест с текстовым сообщением")
    parser.add_argument("--speak", help="Преобразование текста в речь")
    parser.add_argument("--browse", help="URL для просмотра с помощью Browser-Use")
    parser.add_argument("--task", help="Задача для выполнения в браузере", default="собрать информацию")
    
    args = parser.parse_args()
    
    if args.echo:
        print("Тестирование echo_message...")
        result = call_echo_message(args.echo)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif args.speak:
        print("Тестирование speak_text...")
        result = call_speak_text(args.speak)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif args.browse:
        print(f"Тестирование browse_website для {args.browse}...")
        result = call_browse_website(args.browse, args.task)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 