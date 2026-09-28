import importlib

SETUP_APP_MODULE = "src._setup_app"


def reload_setup_app() -> dict:
    """Rilegge _setup_app.py da disco e restituisce ASSETS_LIBRARY, RENDER_DICT, STYLES.

    Il codice viene eseguito in un namespace pulito: se il file contiene errori,
    l'eccezione viene propagata e la configurazione attiva in memoria resta intatta.
    """
    module = importlib.import_module(SETUP_APP_MODULE)

    source_path = module.__file__
    with open(source_path, "r", encoding="utf-8") as f:
        source = f.read()

    namespace = {
        "__name__": SETUP_APP_MODULE,
        "__file__": source_path,
        "__package__": "src",
    }

    exec(compile(source, source_path, "exec"), namespace)

    module.__dict__.update(namespace)

    return {
        "ASSETS_LIBRARY": namespace["ASSETS_LIBRARY"],
        "RENDER_DICT": namespace["RENDER_DICT"],
        "STYLES": namespace["STYLES"],
    }