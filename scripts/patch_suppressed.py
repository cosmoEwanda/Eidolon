import sys
import os
import re
import pathlib

EXTRA = [
    "tkinter", "_tkinter", "tkinter.ttk", "tkinter.messagebox",
    "PySimpleGUI",
    "webbrowser",
    "pandas.io.clipboard",
    "PIL.ImageQt",
    "matplotlib",
    "scipy",
]


def find_pyinstaller_build_main():
    import PyInstaller.building.build_main as bm
    return pathlib.Path(bm.__file__)


def patch():
    path = find_pyinstaller_build_main()
    print(f"Patching: {path}")

    src = path.read_text("utf-8")

    old = "_PRE_SAFE_PACKAGES = ["
    if old not in src:
        print("ERROR: _PRE_SAFE_PACKAGES not found")
        sys.exit(1)

    lines = src.split("\n")
    new_lines = []
    found = False
    already_present = set()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("_PRE_SAFE_PACKAGES = ["):
            new_lines.append(line)
            found = True
            for m in EXTRA:
                if m not in already_present:
                    already_present.add(m)
                    indent = line[:len(line) - len(line.lstrip())] + "    "
                    new_lines.append(f"{indent}'{m}',")
            continue
        if found and stripped == "]":
            found = False
        new_lines.append(line)

    result = "\n".join(new_lines)
    path.write_text(result, "utf-8")

    print("Added to _PRE_SAFE_PACKAGES:")
    for m in EXTRA:
        print(f"  - '{m}'")

    import importlib
    import PyInstaller.building.build_main as bm
    importlib.reload(bm)
    print(f"\n_PRE_SAFE_PACKAGES now has {len(bm._PRE_SAFE_PACKAGES)} entries")


if __name__ == "__main__":
    patch()
