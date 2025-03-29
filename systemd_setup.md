# Настройка автоматического запуска Voice Avatar MCP Server

Для автоматического запуска Voice Avatar MCP Server при загрузке системы можно использовать systemd. Это позволит Cursor всегда иметь доступ к функциям MCP-сервера без необходимости запускать его вручную.

## Шаги для настройки

### 1. Создание службы systemd

Создайте файл конфигурации службы:

```bash
sudo nano /etc/systemd/system/voice-avatar-mcp.service
```

И добавьте следующее содержимое:

```ini
[Unit]
Description=Voice Avatar MCP Server
After=network.target

[Service]
User=cyberkitty
WorkingDirectory=/home/cyberkitty/my_mcp
ExecStart=/usr/bin/python3 /home/cyberkitty/my_mcp/voice_avatar_mcp_starlette.py
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

### 2. Установка зависимостей в системный Python

Чтобы служба могла работать без активации виртуального окружения, установите необходимые зависимости в системный Python:

```bash
sudo pip3 install starlette uvicorn httpx python-dotenv
```

### 3. Включение и запуск службы

```bash
# Перезагрузка конфигурации systemd
sudo systemctl daemon-reload

# Включение автозапуска службы
sudo systemctl enable voice-avatar-mcp.service

# Запуск службы
sudo systemctl start voice-avatar-mcp.service

# Проверка статуса
sudo systemctl status voice-avatar-mcp.service
```

### 4. Просмотр журнала службы

Если вам нужно посмотреть логи сервера:

```bash
sudo journalctl -u voice-avatar-mcp.service -f
```

### 5. Обновление .cursorrules для работы с systemd

Обновите файл `.cursorrules`, изменив раздел о запуске MCP-сервера:

```markdown
## Правила для Cursor
1. MCP-сервер запускается автоматически при загрузке системы через systemd
2. Для проверки статуса MCP-сервера используйте команду: `sudo systemctl status voice-avatar-mcp.service`
3. При обращении к файлам всегда используйте абсолютный путь: `/home/cyberkitty/my_mcp/...`
...
```

## Устранение проблем

### Служба не запускается

Проверьте журнал для получения дополнительной информации:

```bash
sudo journalctl -u voice-avatar-mcp.service
```

### Проблемы с правами доступа

Убедитесь, что пользователь `cyberkitty` имеет доступ ко всем необходимым файлам и каталогам:

```bash
sudo chown -R cyberkitty:cyberkitty /home/cyberkitty/my_mcp
sudo chmod -R 755 /home/cyberkitty/my_mcp
```

### Порт уже используется

Если порт 8000 уже используется другим приложением, измените его в файле `voice_avatar_mcp_starlette.py`, а затем перезапустите службу:

```bash
sudo systemctl restart voice-avatar-mcp.service
```

## Дополнительная настройка для работы с Cursor

После настройки автозапуска службы, убедитесь, что плагин для Cursor правильно настроен на использование URL-адреса MCP-сервера. Проверьте файл `/home/cyberkitty/my_mcp/cursor_plugin/voice_avatar_plugin.py` и убедитесь, что параметр `MCP_SERVER_URL` указывает на `http://127.0.0.1:8000`.

При необходимости, вы также можете настроить переменную среды в файле `.env` в домашнем каталоге пользователя, запускающего Cursor:

```bash
echo "MCP_SERVER_URL=http://127.0.0.1:8000" >> ~/.env
``` 