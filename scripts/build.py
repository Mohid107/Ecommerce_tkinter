import PyInstaller.__main__
import os
import shutil

def build_exe():
    print("Clean build directories...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    print("Running PyInstaller...")
    PyInstaller.__main__.run([
        '../run.py',
        '--name=ShopEasy',
        '--onefile',
        '--windowed',
        '--clean',
        # Add data files if needed here, e.g., --add-data "resources;resources"
    ])
    
    print("Build Complete. Executable is in dist/ShopEasy.exe")

if __name__ == "__main__":
    build_exe()
