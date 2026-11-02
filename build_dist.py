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
    img_data = os.path.join("src", "img") + f"{sep}img"
    dico_data = os.path.join("src", "dico") + f"{sep}dico"
    client_args = [
        sys.executable, "-m", "PyInstaller",
        "--name", "CoviScrabble",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--paths", "src",
        "--add-data", img_data,
        "--add-data", dico_data,
        os.path.join("src", "main_client.py")
    ]
    subprocess.check_call(client_args, cwd=BASE_DIR)

    # 2. Compilation du Serveur (Console)
    print("\n[2/2] Compilation du Serveur (CoviScrabble-Server)...")
    db_data = os.path.join("src", "database.py") + f"{sep}."
    server_args = [
        sys.executable, "-m", "PyInstaller",
        "--name", "CoviScrabble-Server",
        "--console",
        "--noconfirm",
        "--clean",
        "--paths", "src",
        "--add-data", db_data,
        os.path.join("src", "main_server.py")
    ]
    subprocess.check_call(server_args, cwd=BASE_DIR)

    # 3. Copie du guide de démarrage rapide QUICKSTART.txt dans dist/
    quickstart_src = os.path.join(BASE_DIR, "QUICKSTART.txt")
    quickstart_dst = os.path.join(dist_dir, "QUICKSTART.txt")
    if os.path.exists(quickstart_src):
        print("\n[3/3] Copie de QUICKSTART.txt dans dist/...")
        shutil.copy2(quickstart_src, quickstart_dst)

    print("\n=== Compilation terminée avec succès dans le dossier 'dist/' ===")

if __name__ == '__main__':
    build()
