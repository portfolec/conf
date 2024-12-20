# 1. Клонирование репозитория

Склонируйте репозиторий с исходным кодом и тестами:

```
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Установка зависимостей при запуске

```
pip install tkinter
pip install tarfile
pip install argparse
pip install pwd
```

# Создайте виртуальное окружение

```bash
# Активируйте виртуальное окружение
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для MacOS/Linux:
source venv/bin/activate
```


# 3. Структура проекта
Проект содержит следующие файлы и директории:
```bash
unittests.py              # файл для тестирования
virtual_fs.tar           # tar-архив в качестве образа файловой системы
emulator.py                  # файл с программой
log.xml                      #log файл
```

# 4. Запуск проекта
```bash
python emulator.py --script script.txt virtual_fs.tar     # py название файла <стартоый скрипт> <файл с образом файловой системы>
```

# 5 Тесты
```bash
python -m  unittest unttests.py
```
<img width="567" alt="Снимок экрана 2024-12-20 в 15 08 00" src="https://github.com/user-attachments/assets/7143d40c-a62f-4d0a-a7cb-01e54cddf079" />

<img width="337" alt="Снимок экрана 2024-12-20 в 15 15 32" src="https://github.com/user-attachments/assets/f680484c-24ac-45f8-8f42-8842a7d85fc0" />

