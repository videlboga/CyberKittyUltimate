# Интеграция Browser-Use в MCP проект

## Обзор

[Browser-Use](https://github.com/browser-use/browser-use) - это мощный инструмент для подключения ИИ-агентов к браузеру. В нашем проекте Voice Avatar MCP Server мы используем Browser-Use для добавления функциональности автоматизированного взаимодействия с веб-сайтами.

## Возможности

Browser-Use позволяет нашему MCP-серверу:

- Автоматизировать навигацию по веб-сайтам
- Извлекать информацию с веб-страниц
- Заполнять формы и выполнять действия на сайтах
- Делать скриншоты и сохранять информацию
- Выполнять сложные многошаговые задачи в браузере

## Установка

Для использования Browser-Use в проекте установлены следующие компоненты:

```bash
pip install browser-use
pip install playwright
playwright install chromium
```

## Настройка

### API ключи

Для работы Browser-Use требуется API ключ OpenAI. Добавьте свой ключ в файл `.env`:

```
OPENAI_API_KEY=ваш_ключ_здесь
```

Другие провайдеры, которые можно использовать:
- Anthropic (Claude): `ANTHROPIC_API_KEY`
- Google (Gemini): `GEMINI_API_KEY`
- Ollama (локальные модели): не требует ключа

### Использование в MCP-сервере

В нашем MCP-сервере создан инструмент `browse_website`, который принимает URL и описание задачи:

```python
@app.tool("browse_website")
async def browse_website(
    url: Annotated[str, "URL веб-сайта для посещения"],
    task: Annotated[str, "Задача, которую нужно выполнить на сайте"] = "собрать информацию"
) -> Dict[str, Any]:
    # ... реализация ...
```

## Примеры использования

### Через клиентский скрипт

```bash
python test_mcp_client.py --browse "https://example.com" --task "найти информацию о компании и сохранить контакты"
```

### Прямой вызов API

```bash
curl -X POST http://localhost:8000/mcp/tools \
  -H "Content-Type: application/json" \
  -d '{
    "name": "browse_website",
    "parameters": {
      "url": "https://example.com",
      "task": "найти информацию о компании и сохранить контакты"
    }
  }'
```

## Расширение функциональности

Текущая реализация использует GPT-4o, но можно модифицировать код для использования других моделей:

```python
agent = Agent(
    task=f"Посетить сайт {url} и {task}. Сохранить результаты в файл.",
    llm=ChatOpenAI(model="gpt-4o"),  # Можно заменить на другую модель
)
```

## Ограничения

- Требует доступа к API OpenAI или других провайдеров
- Использует значительное количество токенов для работы с большими веб-страницами
- Требует доступ к браузеру и графическому окружению
- Некоторые сайты могут блокировать автоматизированный доступ

## Ресурсы

- [Официальный репозиторий Browser-Use](https://github.com/browser-use/browser-use)
- [Примеры использования](https://github.com/browser-use/browser-use/tree/main/examples)
- [Документация Browser-Use](https://browser-use.com/docs) 