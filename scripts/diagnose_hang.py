import sys
import subprocess
import os

PACKAGES = [
    "tkinter", "_tkinter", "tkinter.ttk", "tkinter.messagebox",
    "PIL", "PIL.Image", "PIL.ImageTk", "PIL.ImageFilter",
    "numpy", "numpy._core._multiarray_umath",
    "pandas", "pandas._libs.lib",
    "requests",
    "urllib3", "urllib3.util.connection",
    "certifi",
    "charset_normalizer",
    "idna",
    "jinja2",
    "markupsafe",
    "reportlab", "reportlab.pdfgen.canvas",
    "dateutil", "dateutil.tz.win",
    "tzdata",
    "json",
    "hashlib",
    "webbrowser",
    "multiprocessing", "multiprocessing.util",
    "ctypes",
    "xml", "xml.etree.ElementTree",
    "sqlite3",
    "setuptools", "setuptools._distutils", "setuptools._vendor",
    "distutils",
    "pkg_resources",
    "inspect",
    "pkgutil",
    "io",
    "os",
    "subprocess",
    "shutil",
    "re",
    "math",
    "collections",
    "enum",
    "typing",
    "functools",
    "itertools",
    "textwrap",
    "dataclasses",
    "pathlib",
    "platform",
    "socket",
    "ssl",
]

TIMEOUT = 10

def try_import(modname):
    code = f"import {modname}; print('OK:' + repr(type({modname})))"
    try:
        r = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        if r.returncode == 0 and r.stdout.startswith("OK:"):
            return True, r.stdout.strip()
        else:
            return False, (r.stderr or r.stdout or "(no output)").strip()
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT - HANGS"
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 60)
    print(f"Diagnosing import hang (timeout={TIMEOUT}s each)")
    print("=" * 60)
    print()

    hanging = []
    ok = []
    failed = []

    for modname in PACKAGES:
        success, msg = try_import(modname)
        if msg == "TIMEOUT - HANGS":
            print(f"  HANG  : {modname}")
            hanging.append(modname)
        elif success:
            print(f"  OK    : {modname}")
            ok.append(modname)
        else:
            print(f"  FAIL  : {modname} -> {msg[:80]}")
            failed.append((modname, msg))

    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"OK:     {len(ok)}/{len(PACKAGES)}")
    print(f"FAIL:   {len(failed)}")
    print(f"HANG:   {len(hanging)}")

    if hanging:
        print()
        print("=" * 60)
        print("HANGING PACKAGES (add to _PRE_SAFE_PACKAGES):")
        for m in hanging:
            print(f"  - '{m}'")
    if failed:
        print()
        print("FAILED (error, not hang):")
        for m, err in failed:
            print(f"  - {m}: {err[:100]}")

    if hanging:
        sys.exit(1)

if __name__ == "__main__":
    main()
