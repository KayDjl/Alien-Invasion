from cx_Freeze import setup, Executable
import os


executables = [Executable("alien_invasion.py", base="Win32GUI" )]


include_files = [
    "score_info/",    # папка с данными
    "images/",  # папка с изображениями
    "sound/",  # папка со звуками

]

# Список всех используемых модулей
packages = ["pygame",
            "os",
            "time",
            "sys"
            ]  

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
