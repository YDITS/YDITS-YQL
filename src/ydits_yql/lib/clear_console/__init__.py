import os


def clear_console(self) -> int:
    if os.name in ("nt", "dos"):
        return os.system(command="cls")
    else:
        return os.system(command="clear")
