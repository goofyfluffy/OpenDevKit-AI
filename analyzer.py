"""Safe, static Python source analysis without executing input code."""
import ast
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass
class Finding:
    line: int
    code: str
    message: str
    severity: str = "info"


def analyze_source(source: str) -> dict:
    findings = []
    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        return {"valid": False, "findings": [asdict(Finding(error.lineno or 1, "SYNTAX", error.msg, "error"))], "functions": [], "classes": []}
    functions = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append(Finding(node.lineno, "BARE_EXCEPT", "Avoid bare except; catch specific exceptions.", "warning"))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
            findings.append(Finding(node.lineno, "DYNAMIC_EXEC", "Review dynamic code execution for security risks.", "warning"))
        if isinstance(node, ast.FunctionDef) and not ast.get_docstring(node):
            findings.append(Finding(node.lineno, "DOCSTRING", f"Consider documenting function '{node.name}'."))
    return {"valid": True, "findings": [asdict(f) for f in sorted(findings, key=lambda f: f.line)], "functions": functions, "classes": classes}


def analyze_file(path: str) -> dict:
    file = Path(path)
    if file.suffix != ".py":
        raise ValueError("Only Python (.py) files are supported")
    if file.stat().st_size > 1_000_000:
        raise ValueError("Files must be 1 MB or smaller")
    return analyze_source(file.read_text(encoding="utf-8"))
