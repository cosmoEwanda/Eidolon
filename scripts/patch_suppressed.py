import sys
import pathlib

EXTRA = [
    "tkinter",
    "_tkinter",
    "tkinter.ttk",
    "tkinter.messagebox",
    "webbrowser",
    "pandas.io.clipboard",
    "PIL.ImageQt",
    "matplotlib",
    "scipy",
]


def patch():
    import PyInstaller.building.build_main as bm
    path = pathlib.Path(bm.__file__)
    print(f"Patching: {path}")

    src = path.read_text("utf-8")

    # PyInstaller 6.21.0 already suppresses PySimpleGUI per issue #8396.
    # We need to add more packages that can also hang on import.
    # Extend the existing suppressed_imports += ['PySimpleGUI'] line
    # so we don't introduce any indentation issues.
    marker = "suppressed_imports += ['PySimpleGUI']"
    if marker not in src:
        print("ERROR: suppressed_imports += ['PySimpleGUI'] not found")
        sys.exit(1)

    # Build the additions, skipping packages already in source
    additions = []
    for m in EXTRA:
        quoted = f"'{m}'"
        if quoted not in src:
            additions.append(quoted)

    if not additions:
        print("All extra packages already present. Nothing to do.")
        return

    extra_str = ", ".join(additions)
    # Extend the existing list literal on the same line
    replacement = marker.replace("]", f", {extra_str}]")
    src = src.replace(marker, replacement, 1)
    path.write_text(src, "utf-8")

    print("Added to suppressed_imports:")
    for m in EXTRA:
        quoted = f"'{m}'"
        if quoted in additions:
            print(f"  - '{m}'")


if __name__ == "__main__":
    patch()
