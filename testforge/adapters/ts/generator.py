import re
from pathlib import Path
from jinja2 import Template

TEST_TEMPLATE = Template("""\
import {{ import_tokens }} from "{{ rel_path }}";

describe("{{ name }}", () => {
  it("smoke", () => {
    const res = {{ name }}();
    expect(res).not.toBeNull();
  });
});
""")

def find_exports(js_path: Path):
    text = js_path.read_text()
    # simplistic: find `export function name` or `export const name =`
    names = set()
    for m in re.finditer(r'export\\s+function\\s+([a-zA-Z0-9_]+)\\s*\\(', text):
        names.add(m.group(1))
    for m in re.finditer(r'export\\s+(?:const|let|var)\\s+([a-zA-Z0-9_]+)\\s*=', text):
        names.add(m.group(1))
    for m in re.finditer(r'export\\s+default\\s+function\\s+([a-zA-Z0-9_]+)?', text):
        if m.group(1):
            names.add(m.group(1))
    return list(names)

def generate_tests_for_target(target: Path):
    target = Path(target)
    out_dir = target / "tests_generated" / "ts"
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for f in target.rglob("*.ts"):
        if f.name.endswith(".d.ts") or "tests_generated" in f.parts:
            continue
        names = find_exports(f)
        if not names:
            continue
        rel = f.relative_to(target).with_suffix('')
        rel_path = "./" + "/".join(rel.parts)
        for name in names:
            import_tokens = name
            content = TEST_TEMPLATE.render(import_tokens=import_tokens, rel_path=rel_path, name=name)
            fname = out_dir / f"test_{f.stem}_{name}.spec.ts"
            fname.write_text(content)
            count += 1
    return count
