import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        "os",
        "traceback",
        "webbrowser",
        "random",
        "platform",
        "json",
        "PySimpleGUI",
        "PIL",
        "tkinter"
    ],
    "include_msvcr":True,
    "excludes": []
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Geometrat",
    version="1.2.0",
    description="Geometrize the images",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            icon='./assets/icon.ico'
        )
    ]
)