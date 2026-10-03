#!/usr/bin/env python
"""
ISBMS Desktop Software PyInstaller Build Automator
Compiles Django project, SQLite DB, templates, static assets into ISBMS_Business_Management_System.exe
"""
import os
import sys
import subprocess
import shutil

def build_exe():
    print("==================================================")
    print("  Building ISBMS Business Management System .exe  ")
    print("==================================================")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, 'inventory', 'static', 'images', 'bms_icon.ico')

    # Data folders to include in executable
    add_data = [
        f"{os.path.join(base_dir, 'inventory', 'templates')}{os.pathsep}inventory/templates",
        f"{os.path.join(base_dir, 'inventory', 'static')}{os.pathsep}inventory/static",
        f"{os.path.join(base_dir, 'db.sqlite3')}{os.pathsep}."
    ]

    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=ISBMS_Business_Management_System",
        "--noconfirm",
        "--onedir",
        "--windowed",
        f"--icon={icon_path}",
    ]

    for item in add_data:
        pyinstaller_cmd.extend(["--add-data", item])

    # Hidden imports for Django and dependencies
    hidden_imports = [
        "django",
        "django.core.management",
        "django.core.management.commands.migrate",
        "django.core.management.commands.collectstatic",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "inventory",
        "inventory.apps",
        "isbms",
        "isbms.urls",
        "isbms.wsgi",
        "isbms.settings",
        "pywebview",
        "bottle",
    ]

    for item in hidden_imports:
        pyinstaller_cmd.extend(["--hidden-import", item])

    pyinstaller_cmd.append("main_desktop.py")

    print(f"[Build Engine] Executing PyInstaller command:\n{' '.join(pyinstaller_cmd)}\n")
    res = subprocess.run(pyinstaller_cmd, cwd=base_dir)

    if res.returncode == 0:
        print("\n==================================================")
        print(" SUCCESS! Software Built Executable Located At:")
        print(f" {os.path.join(base_dir, 'dist', 'ISBMS_Business_Management_System', 'ISBMS_Business_Management_System.exe')}")
        print("==================================================\n")
    else:
        print("\n[Build Error] PyInstaller compilation failed.")

if __name__ == '__main__':
    build_exe()
