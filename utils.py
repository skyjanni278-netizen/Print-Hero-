import os
import platform

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def print_header(titel):
    print("=" * 30)
    print(f"       {titel.upper()}")
    print("=" * 30)