import os
import subprocess

# Список файлов и директорий, которые нужно исключить
exclude_list = [
    "venv", "migrations", "__pycache__", "manage.py", "forum", "bml", "radon.py", "halstead_metrics.py",
    "calculate_metrics.py", "Python3Lexer.py", "Python3Parser.py", "radon_graphics.py",
    "Python3ParserListener.py", "Python3LexerBase.py", "Python3ParserBase.py", "__init__.py"
]


# Функция для обхода файлов в директории
def get_files_to_analyze(root_dir):
    files_to_analyze = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Исключаем папки из exclude_list
        dirnames[:] = [d for d in dirnames if d not in exclude_list]

        for filename in filenames:
            # Проверяем, если файл не в списке исключений, добавляем в список
            if filename not in exclude_list:
                file_path = os.path.join(dirpath, filename)
                files_to_analyze.append(file_path)

    return files_to_analyze


# Путь к корневой директории проекта (измените на свой путь)
root_directory = "."

# Получаем список файлов, которые нужно проанализировать
files = get_files_to_analyze(root_directory)

# Если есть файлы для анализа, запускаем radon
if files:
    # Формируем команду для radon
    command_raw = ["radon", "raw", "-s"] + files
    command_cc = ["radon", "cc", "-s", "-a"] + files

    # Выполняем команду для raw
    subprocess.run(command_raw)

    # Выполняем команду для cc
    subprocess.run(command_cc)
else:
    print("Нет файлов для анализа.")
