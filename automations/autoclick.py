from src.mouse_controller import MouseController
from src.automation import Automation

def autoclick():
    MouseController.click()
    MouseController.wait(1)

def main():
    Automation.loop("Autoclick", autoclick)

if __name__ == "__main__":
    main()
