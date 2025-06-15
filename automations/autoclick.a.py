from src.mouse_controller import MouseController as mc
from src.automation import Automation

def autoclick():
    mc.click()
    mc.wait(1)

def main():
    Automation.loop("Autoclick", autoclick)

if __name__ == "__main__":
    main()
