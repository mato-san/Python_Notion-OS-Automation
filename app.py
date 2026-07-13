import subprocess
import sys
import os
from pystray import Icon, Menu, MenuItem

def run_sync(icon, item):
    script = os.path.join(os.path.dirname(__file__), "sync_database.py")

    subprocess.Popen(
        [sys.executable, script],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

icon = Icon(
    "My App",
    icon_image,
    menu=Menu(
        MenuItem("Run Database Sync", run_sync),
        MenuItem("Quit", quit_app)
    )
)

icon.run()
