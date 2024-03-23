import platform
import shutil
from invoke import task

@task
def build(ctx):
    """
    Build the project for distribution.
    """
    os_name = platform.system()

    # Set icon file based on platform
    if os_name == "Windows":
        icon_file = "icon.ico"
    else:
        icon_file = "icon.png"

    # Set script file
    script_file = "main.py"

    # Run Cython to compile .pyx files
    ctx.run("cythonize -i ray.pyx")
    ctx.run("cythonize -i walls.pyx")

    # Run PyInstaller to create executable
    cmd = f"pyinstaller --windowed --icon {icon_file} --name RayCast --clean --add-data {icon_file}:. --noconfirm {script_file}"
    ctx.run(cmd)

    # Check if PyInstaller completed successfully
    if not shutil.which("RayCast"):
        raise Exception("PyInstaller failed to compile the script.")

    print("Compilation successful.")

@task
def clean(ctx):
    """
    Clean build artifacts.
    """
    ctx.run("rm -rf build dist __pycache__ *.spec")
