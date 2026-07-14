import subprocess
import sys
import os
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

sync_process = None

def run_sync(icon, item):
    global sync_process
    print("Button clicked!")
    if sync_process is None or sync_process.poll() is not None:
        script = os.path.join(os.path.dirname(__file__), "Notion_Python.py")

        sync_process = subprocess.Popen(
            [sys.executable, script],
        )

def create_image():
    image = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill="blue")
    return image

def quit(icon):
    global running
    running = False
    icon.stop()

icon = Icon(
    "My App",
    create_image(),
    menu=Menu(
        MenuItem("Run Database Sync", run_sync),
        MenuItem("Quit", quit)
    )
)

icon.run()
