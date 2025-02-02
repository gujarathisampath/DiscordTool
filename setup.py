from cx_Freeze import setup, Executable

base = None    

executables = [Executable("DiscordTool.py", base=base,icon="icon.ico",shortcut_name="DiscordTool",copyright="Copyright (C) 2025 Sampath")]
build_exe_options = {"excludes": ["tkinter", "PyQt4.QtSql", "sqlite3", 
                                  "scipy.lib.lapack.flapack",
                                  "PyQt4.QtNetwork",
                                  "PyQt4.QtScript",
                                  "numpy.core._dotblas", 
                                  "PyQt5"],
                     "optimize": 2}

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Discord Tool",
    version = "1.1.1", 
    description = 'Discord Server Cloning Tool - Allows copying server channels, roles, settings and emojis to a new server',
    author = 'Sampath',
    executables = executables,
    options = options,
)