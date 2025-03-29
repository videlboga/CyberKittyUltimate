# Полная интеграция Cursor с Voice Avatar MCP Server

## Обзор

Данный документ описывает, как полностью интегрировать AI-ассистент Cursor с нашим Voice Avatar MCP Server. Интеграция позволяет использовать все функции MCP-сервера непосредственно из Cursor, включая синтез речи, автоматизацию браузера и анимацию аватаров.

## Настройка интеграции

### 1. Предварительные требования

- Установленный и настроенный Cursor
- Запущенный MCP-сервер (`./start_mcp.sh`)
- Установленный плагин для Cursor (`cd cursor_plugin && pip install -e .`)

### 2. Подключение плагина в Cursor

1. Откройте настройки Cursor
2. Перейдите в раздел Plugins (Плагины)
3. Добавьте путь к плагину: `/home/cyberkitty/my_mcp/cursor_plugin`
4. Перезапустите Cursor для применения изменений

## Использование функций MCP-сервера в Cursor

### Синтез речи

В Cursor, вы можете использовать функцию синтеза речи двумя способами:

1. **Через Python-код**:
   ```python
   from cursor_plugin.voice_avatar_plugin import speak_text_sync
   
   speak_text_sync("Привет, мир!")
   ```

2. **Через горячую клавишу**:
   - Выделите текст в редакторе
   - Нажмите `Alt+P`

### Автоматизация браузера

Вы можете использовать функцию автоматизации браузера для исследования или выполнения задач в интернете:

```python
from cursor_plugin.voice_avatar_plugin import browse_website_sync

browse_website_sync("https://docs.python.org", "найти информацию о модуле asyncio")
```

### Получение информации об инструментах

Чтобы узнать, какие инструменты доступны на MCP-сервере:

```python
from cursor_plugin.voice_avatar_plugin import get_tools_info_sync

tools = get_tools_info_sync()
print(tools)
```

## Расширение функциональности

Если вы хотите добавить новые функции в MCP-сервер и сделать их доступными через Cursor:

1. Добавьте новый инструмент в `voice_avatar_mcp_starlette.py`
2. Добавьте соответствующий метод в `cursor_plugin/voice_avatar_plugin.py`
3. Обновите `cursor_plugin/cursorrules.json`, добавив новый инструмент

## Устранение неполадок

### MCP-сервер не отвечает

Убедитесь, что MCP-сервер запущен:
```bash
ps aux | grep voice_avatar_mcp
```

Если сервер не запущен, запустите его:
```bash
cd /home/cyberkitty/my_mcp
./start_mcp.sh
```

### Плагин не загружается в Cursor

Проверьте путь к плагину в настройках Cursor и убедитесь, что плагин установлен:
```bash
pip list | grep cursor-voice-avatar-plugin
```

### Ошибки при вызове инструментов

Проверьте журнал ошибок MCP-сервера для получения дополнительной информации:
```bash
tail -n 50 /home/cyberkitty/my_mcp/mcp_server.log
```

## Примеры интеграции в рабочий процесс

### Пример 1: Генерация комментариев к коду с речью

```python
# Выделите блок кода в Cursor, затем выполните:
code = """def calculate_sum(a, b):
    return a + b"""

comment = cursor.ai.explain_code(code)  # Функция Cursor AI для объяснения кода
from cursor_plugin.voice_avatar_plugin import speak_text_sync
speak_text_sync(comment)  # Озвучивание объяснения
```

### Пример 2: Исследование документации с помощью браузера

```python
from cursor_plugin.voice_avatar_plugin import browse_website_sync

# Исследование документации по нужной библиотеке
result = browse_website_sync("https://docs.python.org", "найти информацию о concurrent.futures")
print(result)
```

### Пример 3: Генерация документации с помощью AI и озвучивание

```python
# Генерация документации с помощью Cursor AI
doc = cursor.ai.generate_docstring(selected_function)

# Озвучивание документации
from cursor_plugin.voice_avatar_plugin import speak_text_sync
speak_text_sync(doc)
``` 