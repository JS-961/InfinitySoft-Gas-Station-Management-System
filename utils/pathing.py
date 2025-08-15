import sys, os

def resource_path(rel_path: str) -> str:
    try:
        base_path = sys._MEIPASS  
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)
