#!/usr/bin/env python3
#coding:utf-8
"""
build_dist.py - Script de packaging universel (macOS, Windows, Linux) avec PyInstaller.
Prépare des exécutables autonomes pour le Client (GUI) et le Serveur.
"""

import sys
import os
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def build():
    is_windows = sys.platform.startswith('win')
    is_macos = sys.platform == 'darwin'
    sep = ';' if is_windows else ':'

    print(f"=== Début de la construction pour la plateforme : {sys.platform} ===")

    # Vérification de PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("Installation de PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    dist_dir = os.path.join(BASE_DIR, "dist")
    build_dir = os.path.join(BASE_DIR, "build")

    # Nettoyage préalable
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    # 1. Compilation du Client (GUI sans console)
    print("\n[1/2] Compilation du Client GUI (CoviScrabble)...")
    client_args = [
        sys.executable, "-m", "PyInstaller",
        "--name", "CoviScrabble",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--add-data", f"img{sep}img",
        "--add-data", f"dico{sep}dico",
        "main_client.py"
    ]
    subprocess.check_call(client_args, cwd=BASE_DIR)

    # 2. Compilation du Serveur (Console)
    print("\n[2/2] Compilation du Serveur (CoviScrabble-Server)...")
    server_args = [
        sys.executable, "-m", "PyInstaller",
        "--name", "CoviScrabble-Server",
        "--console",
        "--noconfirm",
        "--clean",
        "--add-data", f"database.py{sep}.",
        "main_server.py"
    ]
    subprocess.check_call(server_args, cwd=BASE_DIR)

    print("\n=== Compilation terminée avec succès dans le dossier 'dist/' ===")

if __name__ == '__main__':
    build()
