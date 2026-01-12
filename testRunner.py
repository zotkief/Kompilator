#!/usr/bin/env python3
from pathlib import Path
import subprocess

BASE_PATH = Path("/home/zotkief/Desktop/mw2025")

# Sprawdzenie folderu
if not BASE_PATH.exists():
    print(f"Folder nie istnieje: {BASE_PATH}")
    exit(1)

# Szukamy plików .imp
imp_files = list(BASE_PATH.glob("*.imp"))
if not imp_files:
    print("Nie znaleziono plików .imp w folderze")
    exit(1)

for input_file in imp_files:
    output_file = input_file.with_suffix("")  # usuwa .imp

    cmd = [
        "python3",
        "-m",
        "kompilator.main",
        str(input_file.resolve()),  # absolutna ścieżka
        str(output_file.resolve())  # absolutna ścieżka
    ]
    print(" ".join(cmd)) 

    print(f"Uruchamiam: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"✔ Gotowe: {input_file.name} -> {output_file.name}")
    else:
        print(f"❌ Błąd przy pliku: {input_file.name}")
