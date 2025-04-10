# Voice Avatar MCP Plugin для Cursor

Этот плагин позволяет управлять Voice Avatar MCP сервером прямо из Cursor, облегчая создание голосового интерфейса и анимированных персонажей.

## Установка

1. Убедитесь, что MCP-сервер запущен на `http://127.0.0.1:8000`
2. Установите плагин в Cursor:

```bash
cd ~/my_mcp/cursor_plugin
pip install -e .
```

3. Добавьте путь к плагину в настройки Cursor:

```
Настройки > Plugins > Добавить путь к плагину: /home/cyberkitty/my_mcp/cursor_plugin
```

## Использование в Cursor

После установки плагина, вы можете использовать следующие команды в Cursor:

### Преобразование текста в речь

```python
# Синтезировать речь с использованием стандартной модели
speak_text("Привет, мир!")

# Или с указанием конкретной модели голоса
speak_text("Привет, мир!", "ru_RU-irina-medium")
```

### Тестирование (эхо-ответ)

```python
# Отправить тестовое сообщение
echo_message("Привет, это тестовое сообщение")
```

### Автоматизация браузера

```python
# Посетить сайт и выполнить задачу
browse_website("https://example.com", "найти контактную информацию")
```

### Получение информации о доступных инструментах

```python
# Получить список всех доступных инструментов
tools_info = get_tools_info()
print(tools_info)
```

## Горячие клавиши

Плагин добавляет следующие горячие клавиши для быстрого доступа к функциям:

| Горячая клавиша | Команда | Описание |
|-----------------|---------|----------|
| `Alt+P` | speak_selection | Преобразовать выделенный текст в речь |
| `Alt+B` | browse_selection | Выполнить поиск информации по выделенному тексту |
| `Alt+E` | explain_selection | Объяснить выделенный код и озвучить объяснение |
| `Alt+I` | get_tools | Получить список доступных инструментов |

Эти горячие клавиши настраиваются в файле `hotkeys.json`.

## Расширенные функции

Плагин теперь включает расширенные функции для обработки выделенного текста и кода:

### Обработка выделенного текста

```python
# Импорт функции
from cursor_plugin.extensions import process_selected_text

# Преобразование текста в речь
result = process_selected_text("Привет, мир!", "speak")

# Поиск информации
result = process_selected_text("Python asyncio", "browse")

# Объяснение кода
code = """async def hello_world():
    print('Hello, World!')"""
result = process_selected_text(code, "explain")
```

### Выполнение команд

```python
# Импорт функции
from cursor_plugin.extensions import execute_cursor_command

# Выполнение команды
result = execute_cursor_command("speak_selection")
```

## Примеры интеграции в workflow Cursor

### Пример 1: Генерация речи для кода

```python
def explain_code_with_voice(code_snippet):
    """
    Анализирует код и объясняет его голосом.
    """
    explanation = analyze_code(code_snippet)  # Функция анализа кода в Cursor
    speak_text(explanation)
    return explanation
```

### Пример 2: Веб-исследование с браузером

```python
def research_topic(topic):
    """
    Исследует тему в интернете и возвращает результаты.
    """
    search_url = f"https://www.google.com/search?q={topic}"
    results = browse_website(search_url, f"исследовать тему '{topic}' и собрать основную информацию")
    return results
```

### Пример 3: Голосовое оповещение о завершении задачи

```python
def long_running_task():
    """
    Выполняет долгую задачу и оповещает о завершении голосом.
    """
    # ... код долгой задачи ...
    speak_text("Задача успешно завершена!")
    return result
```

## Меню и контекстные команды

Плагин добавляет следующие пункты меню в Cursor:

- Основное меню: `Инструменты > Voice Avatar MCP`
  - Преобразовать выделенное в речь
  - Найти информацию
  - Объяснить код
  - Получить список инструментов

- Контекстное меню редактора: `Voice Avatar`
  - Преобразовать в речь
  - Найти информацию
  - Объяснить код

## Расширение плагина

Вы можете добавить новые инструменты в плагин:

1. Добавьте новый инструмент в файл MCP-сервера `voice_avatar_mcp_starlette.py`
2. Добавьте соответствующие методы в файл `voice_avatar_plugin.py`
3. Обновите файл `extensions.py` для поддержки новой функциональности
4. Добавьте новую горячую клавишу в `hotkeys.json` при необходимости

## Решение проблем

- Если горячие клавиши не работают, проверьте файл `hotkeys.json` и перезапустите Cursor
- Если функции не отвечают, убедитесь, что MCP-сервер запущен (`sudo systemctl status voice-avatar-mcp.service`)
- Для отладки используйте `print()` в функциях и проверяйте логи MCP-сервера

## Дополнительная информация

Дополнительную информацию об интеграции с Cursor можно найти в файле `/home/cyberkitty/my_mcp/cursor_plugin/cursor_integration.md`. 