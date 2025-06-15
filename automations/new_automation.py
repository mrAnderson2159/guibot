from sys import argv
from os.path import exists
from os import system
import platform
from pathlib import Path
import subprocess

def open_with_vscode(file: str):
    """
    Open a file with Visual Studio Code based on the operating system.

    :param file: Path to the file to be opened.
    """
    system_platform = platform.system()
    filepath = Path(file).resolve()

    if system_platform == "Darwin":  # macOS
        subprocess.run(["open", "-a", "Visual Studio Code", str(filepath)])
    elif system_platform == "Windows":
        subprocess.run(["start", "", str(filepath)], shell=True)
    elif system_platform == "Linux":
        # Fall back to 'code' or xdg-open
        try:
            subprocess.run(["code", str(filepath)])
        except FileNotFoundError:
            subprocess.run(["xdg-open", str(filepath)])
    else:
        print(f"Impossibile aprire il file su sistema non riconosciuto: {system_platform}")

def create_automation(automation_name: str, automation_type: str):
    """
    Create a new automation file with the specified name and a specific automation type
    in the automations directory.

    :param automation_name: Name of the new automation (without .py extension).
    :param automation_type: Type of automation (e.g., 'loop', 'keystroke').
    """
    filename = f"automations/{automation_name}.py"
    content = (f"""# Automation: {automation_name}
from src.mouse_controller import MouseController
from src.automation import Automation
from src.point import Point

def dummy_automation():
     # Your automation code here
     pass

def main():
     Automation.{automation_type}("dummy_automation", dummy_automation)

if __name__ == "__main__":
     main()
                """)

    if exists(filename):
        print(f"Automation '{automation_name}' already exists.")
        return

    with open(filename, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python new_automation.py <automation_name> <loop|keystroke>")
        exit(1)

    automation_name, automation_type = argv[1:]

    if automation_type not in ['loop', 'keystroke']:
        print("Invalid automation type. Use 'loop' or 'keystroke'.")
        exit(1)

    create_automation(automation_name, automation_type)
    open_with_vscode(f"automations/{automation_name}.py")
