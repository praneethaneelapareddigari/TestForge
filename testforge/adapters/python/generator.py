import ast
from pathlib import Path
from jinja2 import Template

TEST_TEMPLATE = Template("""\
import pytest
from {{ import_path }} import {{ name }}

def test_{{ name }}_smoke():
    # auto-generated smoke test by TestForge
    res = {{ name }}()
    assert res is not None
""")

def find_callables(py_file: Path):
    src = py_file.read_text()
    tree = ast.parse(src)
    names = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                names.append(node.name)
        if isinstance(node, ast.ClassDef):
            # include class constructor/test target
            names.append(node.name)
    return names

def generate_tests_for_target(target: Path):
    target = Path(target)
    out_dir = target / "tests_generated"
    out_dir.mkdir(exist_ok=True)
    count = 0
    for py in target.rglob("*.py"):
        # skip tests and generated outputs
        if py.name.startswith("test_") or "tests_generated" in py.parts:
            continue
        names = find_callables(py)
        if not names:
            continue
        rel = py.relative_to(target).with_suffix("")
        import_path = ".".join(rel.parts)
        for name in names:
            content = TEST_TEMPLATE.render(import_path=import_path, name=name)
            fname = out_dir / f"test_{py.stem}_{name}.py"
            fname.write_text(content)
            count += 1
    return count
