from cx_Freeze import setup, Executable
import os

# Замените "main.py" на имя вашего основного файла
executables = [Executable("alien_invasion.py", base="Win32GUI" )]

# Укажите все необходимые файлы и директории
include_files = [
    "score_info/",    # папка с данными
    "images/",  # папка с изображениями
    "sound/",  # папка со звуками
    # Добавьте все необходимые папки и файлы
]

# Список всех используемых модулей
packages = ["pygame",
            "os",
            "time",
            "sys"
            ]  # Замените на ваши пакеты

options = {
    'build_exe': {
        'packages': packages,
        'include_files': include_files,
    }
}

setup(
    name="Alien Invasion",
    version="1.0",
    description="PolozkovPython3",
    options=options,
    executables=executables
)