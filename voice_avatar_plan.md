# План разработки MCP-сервера для голосового интерфейса с анимированным персонажем

## 📋 Инструкция по использованию плана

- [ ] Отметь выполненные пункты галочкой
- [ ] Добавляй комментарии о ходе выполнения каждого пункта (проблемы, решения, особенности)
- [ ] Фиксируй даты выполнения задач
- [ ] Сохраняй все команды, которые использовал для установки/настройки

## 🔍 Общая информация о системе

- **CPU:** 16 ядер
- **RAM:** 31 ГБ
- **GPU:** NVIDIA GeForce RTX 3070 Ti (8 ГБ VRAM)
- **CUDA:** 12.6
- **OS:** Ubuntu с ядром 6.11.0-21-generic
- **Python:** 3.12.7

## 🗂️ Структура проекта

```
~/my_mcp/
  ├── voice_avatar_mcp.py       # Основной MCP-сервер
  ├── requirements.txt          # Зависимости для MCP-сервера
  ├── models/                   # Директория для моделей
  │   ├── tts/                  # Модели для TTS
  │   └── avatars/              # Ресурсы для аватаров
  ├── output/                   # Директория для выходных файлов
  ├── assets/                   # Шаблоны аватаров
  └── docs/                     # Документация
```

## 📦 Ресурсы и ссылки

### TTS (Генерация голоса)
- [ ] Репозиторий Piper: https://github.com/rhasspy/piper
- [ ] Голосовые модели Piper: https://github.com/rhasspy/piper/releases
- [ ] Русские голоса Piper: https://rhasspy.github.io/piper-samples/
- [ ] Документация Piper: https://github.com/rhasspy/piper/blob/master/USAGE.md

### Анимация персонажей
- [ ] Репозиторий V-Express: https://github.com/tencent-ailab/V-Express
- [ ] Документация V-Express: https://github.com/tencent-ailab/V-Express/blob/main/README.md
- [ ] Примеры изображений для аватаров: https://github.com/tencent-ailab/V-Express/tree/main/examples

### MCP-сервер
- [ ] Документация по MCP: https://docs.cursor.com/context/model-context-protocol
- [ ] Примеры MCP серверов: https://github.com/modelcontextprotocol/server-python-examples

## 📅 План разработки

### 1. Подготовка среды разработки

- [ ] Создать директорию проекта и структуру
  ```bash
  mkdir -p ~/my_mcp/{models/{tts,avatars},output,assets,docs}
  ```
- [ ] Настроить виртуальное окружение Python
  ```bash
  cd ~/my_mcp
  python3 -m venv venv
  source venv/bin/activate
  ```
- [ ] Обновить pip и установить базовые инструменты
  ```bash
  pip install --upgrade pip wheel setuptools
  ```

### 2. Установка и настройка Piper TTS

- [ ] Установить pipx (если еще не установлен)
  ```bash
  sudo apt install python3-pipx
  pipx ensurepath
  # Перезапустить терминал или выполнить:
  source ~/.bashrc
  ```
- [ ] Установить Piper TTS
  ```bash
  pipx install piper-tts
  ```
- [ ] Установить необходимые системные зависимости
  ```bash
  sudo apt install espeak-ng-data ffmpeg
  ```
- [ ] Скачать русские голосовые модели
  ```bash
  mkdir -p ~/.local/share/piper-tts/piper-voices
  cd ~/.local/share/piper-tts/piper-voices
  wget https://github.com/rhasspy/piper/releases/download/v0.0.2/ru_RU-irina-medium.onnx
  wget https://github.com/rhasspy/piper/releases/download/v0.0.2/ru_RU-irina-medium.onnx.json
  ```
- [ ] Протестировать Piper
  ```bash
  echo "Привет, мир!" | piper --model ~/.local/share/piper-tts/piper-voices/ru_RU-irina-medium.onnx --output_file ~/my_mcp/output/test.wav
  aplay ~/my_mcp/output/test.wav
  ```

### 3. Установка и настройка V-Express

- [ ] Клонировать репозиторий V-Express
  ```bash
  git clone https://github.com/tencent-ailab/V-Express.git ~/V-Express
  cd ~/V-Express
  ```
- [ ] Создать виртуальное окружение для V-Express
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- [ ] Установить PyTorch с поддержкой CUDA
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
  ```
- [ ] Установить зависимости V-Express
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Загрузить тестовые изображения для аватаров
  ```bash
  # Скопировать примеры из репозитория в assets
  mkdir -p ~/my_mcp/assets/images
  cp -r ~/V-Express/examples/* ~/my_mcp/assets/images/
  ```
- [ ] Протестировать V-Express
  ```bash
  # Запустить с тестовым изображением и аудио
  cd ~/V-Express
  source venv/bin/activate
  python app.py
  # Через GUI загрузить изображение и звуковой файл
  ```

### 4. Разработка MCP-сервера

- [ ] Установить MCP зависимости
  ```bash
  cd ~/my_mcp
  source venv/bin/activate
  pip install modelcontextprotocol pydantic
  ```
- [ ] Создать файл requirements.txt
  ```bash
  pip freeze > requirements.txt
  ```
- [ ] Создать файл voice_avatar_mcp.py со скриптом MCP-сервера
  ```python
  # Содержимое файла voice_avatar_mcp.py
  import os
  import subprocess
  import tempfile
  import time
  from modelcontextprotocol.server import ModelContextProtocolServer, Tool

  class VoiceAvatarServer(ModelContextProtocolServer):
      def __init__(self):
          super().__init__()
          
          # Директории
          self.v_express_dir = os.path.expanduser("~/V-Express")
          self.output_dir = os.path.expanduser("~/my_mcp/output")
          
          # Создаем директорию для выходных файлов
          os.makedirs(self.output_dir, exist_ok=True)
          
          # Регистрация инструментов
          self.register_tool(
              "speak_text", 
              self.speak_text,
              "Преобразует текст в речь с помощью Piper TTS"
          )
          
          self.register_tool(
              "animate_avatar", 
              self.animate_avatar,
              "Создает анимированного персонажа из изображения и аудио"
          )
          
          self.register_tool(
              "speak_with_avatar", 
              self.speak_with_avatar,
              "Создает видео анимированного персонажа, озвучивающего текст"
          )
          
      async def speak_text(self, text, voice_model="ru_RU-irina-medium"):
          """Генерирует речь из текста"""
          output_file = f"{self.output_dir}/speech_{int(time.time())}.wav"
          
          # Создаем временный файл для текста
          with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
              temp.write(text)
              temp_path = temp.name
          
          # Используем Piper для генерации речи
          command = f'cat {temp_path} | piper --model ~/.local/share/piper-tts/piper-voices/{voice_model}.onnx --output_file {output_file}'
          subprocess.run(command, shell=True)
          
          # Удаляем временный файл
          os.unlink(temp_path)
          
          return {"audio_path": output_file}
      
      async def animate_avatar(self, image_path, audio_path, output_path=None):
          """Создает анимированного персонажа из изображения и аудио"""
          if output_path is None:
              output_path = f"{self.output_dir}/avatar_{int(time.time())}.mp4"
          
          # Активируем виртуальное окружение и используем V-Express
          command = f'cd {self.v_express_dir} && source venv/bin/activate && python run.py --image {image_path} --audio {audio_path} --output {output_path}'
          subprocess.run(command, shell=True)
          
          return {"video_path": output_path}
      
      async def speak_with_avatar(self, text, image_path, voice_model="ru_RU-irina-medium"):
          """Создает видео анимированного персонажа, озвучивающего текст"""
          # Генерируем речь
          audio_result = await self.speak_text(text, voice_model)
          audio_path = audio_result["audio_path"]
          
          # Создаем видео с аватаром
          output_path = f"{self.output_dir}/talking_avatar_{int(time.time())}.mp4"
          video_result = await self.animate_avatar(image_path, audio_path, output_path)
          
          return {
              "video_path": video_result["video_path"],
              "audio_path": audio_path
          }

  # Запуск сервера
  if __name__ == "__main__":
      server = VoiceAvatarServer()
      server.start()
  ```

- [ ] Создать скрипт запуска MCP-сервера start_mcp.sh
  ```bash
  #!/bin/bash
  cd ~/my_mcp
  source venv/bin/activate
  python voice_avatar_mcp.py
  ```
- [ ] Сделать скрипт исполняемым
  ```bash
  chmod +x ~/my_mcp/start_mcp.sh
  ```

### 5. Настройка Cursor для использования MCP-сервера

- [ ] Открыть настройки Cursor
  - Перейти в Settings > Features > MCP > Add New MCP Server
- [ ] Добавить новый MCP-сервер
  - Имя: Voice Avatar
  - Тип: command
  - Команда: /home/cyberkitty/my_mcp/start_mcp.sh
- [ ] Сохранить настройки
- [ ] Добавить правила для AI в настройках Cursor:
  ```
  Для генерации голоса используй инструмент speak_text.
  Для создания анимированного персонажа используй инструмент animate_avatar.
  Для создания видео с говорящим персонажем используй инструмент speak_with_avatar.
  
  Для speak_with_avatar требуется указать текст и путь к изображению.
  Примеры изображений находятся в директории /home/cyberkitty/my_mcp/assets/images.
  ```

### 6. Тестирование системы

- [ ] Проверить работу TTS (Piper)
  - Запустить Cursor
  - Открыть Agent и попросить "Сгенерируй речь с текстом 'Привет, мир!'"
  - Проверить создание аудиофайла в ~/my_mcp/output/
- [ ] Проверить работу анимации (V-Express)
  - В Cursor попросить "Создай анимированного персонажа из изображения /home/cyberkitty/my_mcp/assets/images/example.jpg и аудио /home/cyberkitty/my_mcp/output/speech_XXXX.wav"
  - Проверить создание видеофайла в ~/my_mcp/output/
- [ ] Проверить комбинированную работу
  - В Cursor попросить "Создай видео, где персонаж говорит 'Привет, мир!', используя изображение /home/cyberkitty/my_mcp/assets/images/example.jpg"
  - Проверить создание видеофайла в ~/my_mcp/output/

### 7. Оптимизация и дополнительные функции

- [ ] Оптимизировать производительность V-Express
  ```bash
  # Настроить параметры CUDA для оптимальной работы GPU
  cd ~/V-Express
  source venv/bin/activate
  # Отредактировать параметры в app.py или config.py
  ```
- [ ] Добавить кэширование для часто используемых фраз
  - Модифицировать speak_text в voice_avatar_mcp.py для проверки кэша
- [ ] Добавить поддержку других языковых моделей
  - Скачать дополнительные модели для Piper
  - Обновить MCP-сервер для поддержки выбора языка
- [ ] Создать простой веб-интерфейс для просмотра созданных файлов
  ```bash
  cd ~/my_mcp
  source venv/bin/activate
  pip install flask
  # Создать простое веб-приложение на Flask
  ```

## 📝 Заметки и решения проблем

### Установка Piper TTS
- **Проблема:** [Опиши здесь проблему]
- **Решение:** [Опиши здесь решение]

### Установка V-Express
- **Проблема:** [Опиши здесь проблему]
- **Решение:** [Опиши здесь решение]

### Интеграция с MCP
- **Проблема:** [Опиши здесь проблему]
- **Решение:** [Опиши здесь решение]

### Другие заметки:
- [Добавь сюда любые заметки о ходе работы]

## 🛠️ Дополнительные материалы

- Документация по Piper TTS: [ссылка на документацию]
- Примеры настройки V-Express: [ссылка на примеры]
- Описание ошибок и решений: [ссылка на форум или базу знаний]
- Другие полезные материалы: [ссылки]

## 🔄 Обновления и версионность

- **Версия 1.0** - Базовая функциональность
- **Версия 1.1** - Добавлена поддержка кэширования
- **Версия 1.2** - Добавлен веб-интерфейс
- **Версия 2.0** - Полная интеграция с Cursor и настраиваемые шаблоны аватаров 