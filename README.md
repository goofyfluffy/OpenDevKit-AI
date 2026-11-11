# OpenDevKit AI

A **local-first, open-source developer toolkit** for inspecting Python source code. Version 0.1.0 provides a static analyzer, JSON CLI output, automated tests, and an optional local Ollama explanation function.

> Early-stage prototype. Not a replacement for a security audit, professional code review, or mature linters.

## Features
- Parse Python files without running their contents.
- Report syntax errors, bare `except` handlers, and calls to `eval` / `exec`.
- Identify functions, classes, and missing function docstrings.
- Export machine-readable JSON from the command line.
- Optionally ask an Ollama model running on your own computer to explain source code.

## Install
Requires Python 3.10+.

```bash
python -m pip install -e .
opendevkit example.py
```

Or without installation:

```bash
python -m opendevkit.cli example.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Optional local AI
Install and run [Ollama](https://ollama.com/) locally, pull a supported model such as `gemma3:4b`, then use:

```python
from opendevkit.ollama import explain_code
print(explain_code('def add(a, b): return a + b'))
```

The Ollama integration is optional, not called by the CLI, and requires a locally running server. No cloud AI API is required.

## Roadmap
- More static analysis rules and configurable rule sets
- Interactive web UI
- Safe multi-file project summaries
- CI integrations and editor support

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions are voluntary and reviewed on merit. No claims of external adoption or contributors are made.

## License
MIT — see [LICENSE](LICENSE).
