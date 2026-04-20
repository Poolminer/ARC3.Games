import json
import os
import tempfile
from collections import OrderedDict
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from pathlib import Path

PORT = 8000

# Project paths
ROOT_DIR = Path(__file__).resolve().parent
ENVIRONMENT_DIR = ROOT_DIR / "environment_files"
PYSCRIPT_JSON_PATH = ROOT_DIR / "pyscript.json"

# Fixed PyScript packages
PACKAGES = ["arcengine"]

# Files/directories to ignore in addition to dotfiles
IGNORED_NAMES = {
    "__pycache__",
}

# Optional extra suffixes to ignore
IGNORED_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
}


def is_hidden_or_ignored(path: Path, root: Path) -> bool:
    """
    Return True if the path itself, or any path component below `root`,
    is hidden or explicitly ignored.

    Hidden means: basename starts with '.'
    """
    rel_parts = path.relative_to(root).parts
    for part in rel_parts:
        if part.startswith(".") or part in IGNORED_NAMES:
            return True
    return False


def discover_environment_files(root: Path) -> OrderedDict[str, str]:
    """
    Recursively discover files under `root` and build a PyScript `files`
    mapping where virtual path == local path.

    Example mapping entry:
        "./environment_files/foo/bar.py": "./environment_files/foo/bar.py"
    """
    files: list[str] = []

    if not root.exists():
        return OrderedDict()

    for current_root, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        current_root_path = Path(current_root)

        # Prune hidden/ignored directories in-place so os.walk does not enter them
        dirnames[:] = sorted(
            d
            for d in dirnames
            if not is_hidden_or_ignored(current_root_path / d, root)
        )

        for filename in sorted(filenames):
            file_path = current_root_path / filename

            if is_hidden_or_ignored(file_path, root):
                continue

            if file_path.suffix in IGNORED_FILE_SUFFIXES:
                continue

            # Build a manifest path relative to the project root, not just environment_files
            rel_to_project = file_path.relative_to(ROOT_DIR).as_posix()
            manifest_path = f"./{rel_to_project}"
            files.append(manifest_path)

    files.sort()

    return OrderedDict((path, path) for path in files)


def build_pyscript_config() -> OrderedDict:
    """
    Build the full PyScript config with deterministic key order.
    """
    config = OrderedDict()
    config["packages"] = PACKAGES
    config["files"] = discover_environment_files(ENVIRONMENT_DIR)
    return config


def serialize_config(config: dict) -> str:
    """
    Serialize config deterministically so string comparison is stable.
    """
    return json.dumps(config, indent=4, ensure_ascii=False) + "\n"


def atomic_write_text(path: Path, content: str) -> None:
    """
    Atomically replace `path` with `content`.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        delete=False,
        prefix=path.name + ".",
        suffix=".tmp",
    ) as tmp_file:
        tmp_file.write(content)
        temp_name = tmp_file.name

    os.replace(temp_name, path)


def sync_pyscript_json() -> str:
    """
    Build the current PyScript JSON, compare it with the on-disk file,
    and rewrite the file only if the content changed.

    Returns the generated JSON string.
    """
    config = build_pyscript_config()
    new_json = serialize_config(config)

    old_json = None
    if PYSCRIPT_JSON_PATH.exists():
        old_json = PYSCRIPT_JSON_PATH.read_text(encoding="utf-8")

    if old_json != new_json:
        atomic_write_text(PYSCRIPT_JSON_PATH, new_json)
        print(f"Updated {PYSCRIPT_JSON_PATH.name}")
    else:
        print(f"{PYSCRIPT_JSON_PATH.name} is up to date")

    return new_json


class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        # Serve a dynamically generated virtual /pyscript.json
        if self.path == "/pyscript.json":
            try:
                content = sync_pyscript_json().encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as exc:
                error = f'{{"error": "Failed to generate pyscript.json", "details": "{str(exc)}"}}'
                error_bytes = error.encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(error_bytes)))
                self.end_headers()
                self.wfile.write(error_bytes)
            return

        super().do_GET()


def main():
    if not ENVIRONMENT_DIR.exists():
        print(f"Warning: {ENVIRONMENT_DIR} does not exist yet")

    # Keep the on-disk file in sync at startup too
    sync_pyscript_json()

    with TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Serving at http://127.0.0.1:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()