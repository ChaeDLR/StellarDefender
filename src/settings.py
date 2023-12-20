from os import getcwd
from os.path import abspath


width: int = 1280

height: int = 720

size: tuple = (width, height)

assets_path: str = abspath(f"{getcwd()}/src/assets")

main_menu_theme: str = "ull_theme.wav"