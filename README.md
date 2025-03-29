# CyberKittyUltimate - MCP сервер с голосовым интерфейсом и анимированными персонажами

![Версия](https://img.shields.io/badge/версия-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.12%2B-brightgreen)
![Лицензия](https://img.shields.io/badge/лицензия-MIT-green)

## Описание

CyberKittyUltimate - это современный MCP (Machine Control Protocol) сервер для создания голосовых интерфейсов с анимированными персонажами. Проект разработан для интеграции различных технологий голосового синтеза и визуализации в единую экосистему, управляемую через удобный API.

## Особенности

- 🎙 **Синтез речи** с использованием Piper TTS
- 🌐 **Автоматизация браузера** через Browser-Use
- 👤 **Анимация персонажей** с помощью V-Express
- 🔌 **Плагин для Cursor** с полной интеграцией
- 🚀 **Запуск как системная служба** с использованием systemd

## Технологии

- **Python 3.12+**
- **Piper TTS** для синтеза речи
- **Browser-Use** для автоматизации браузера
- **MCP Protocol** для взаимодействия с другими приложениями
- **V-Express** для анимации персонажей
- **NVIDIA CUDA 12.6** для ускорения обработки
- **PyTorch** для нейронных моделей

## Структура проекта

```
CyberKittyUltimate/
├── voice_avatar_mcp_starlette.py  # Основной MCP-сервер
├── start_mcp.sh                   # Скрипт запуска сервера
├── cursor_plugin/                 # Плагин для Cursor
│   ├── voice_avatar_plugin.py     # API для интеграции с Cursor
│   ├── extensions.py              # Расширенные функции
│   ├── hotkeys.json               # Конфигурация горячих клавиш
│   └── README.md                  # Документация по плагину
├── models/                        # Модели для синтеза речи и аватаров
│   ├── tts/                       # Модели TTS
│   └── avatars/                   # Ресурсы для аватаров
├── output/                        # Директория для выходных файлов
└── docs/                          # Документация
```

## Установка

```bash
# Клонирование репозитория
git clone https://github.com/videlboga/CyberKittyUltimate.git
cd CyberKittyUltimate

# Создание и активация виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Установка плагина для Cursor
cd cursor_plugin
pip install -e .
cd ..
```

## Запуск

```bash
# Запуск MCP-сервера
./start_mcp.sh

# Или вручную
python3 voice_avatar_mcp_starlette.py
```

## Использование

### Синтез речи

```python
from cursor_plugin.voice_avatar_plugin import speak_text_sync

# С использованием стандартной модели
speak_text_sync("Привет, мир!")

# С указанием конкретной модели голоса
speak_text_sync("Привет, мир!", "ru_RU-irina-medium")
```

### Автоматизация браузера

```python
from cursor_plugin.voice_avatar_plugin import browse_website_sync

# Поиск информации
browse_website_sync("https://example.com", "найти контактную информацию")
```

## Интеграция с Cursor

Подробная информация об интеграции с Cursor доступна в файле [cursor_plugin/cursor_integration.md](cursor_plugin/cursor_integration.md).

## Настройка автозапуска

Инструкции по настройке автоматического запуска с помощью systemd доступны в файле [systemd_setup.md](systemd_setup.md).

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

## Авторы

- **CyberKitty** - *Основной разработчик*
