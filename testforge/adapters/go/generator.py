import re
from pathlib import Path
from jinja2 import Template

TEST_TEMPLATE = Template("""\
package {{ pkg }}

import "testing"

func Test{{ func_name }}_smoke(t *testing.T) {
    // generated smoke test
    _ = {{ func_name }}()
}
""")

def parse_go_file(path: Path):
    text = path.read_text()
    # find package
    m = re.search(r'package\s+([a-zA-Z_][a-zA-Z0-9_]*)', text)
    pkg = m.group(1) if m else "main"
    # find exported functions (capitalized)
    funcs = re.findall(r'func\s+([A-Z][A-Za-z0-9_]*)\s*\\(', text)
    return pkg, funcs

def generate_tests_for_target(target: Path):
    target = Path(target)
    out_dir = target / "tests_generated" / "go"
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for g in target.rglob("*.go"):
        if g.name.endswith("_test.go") or "tests_generated" in g.parts:
            continue
        pkg, funcs = parse_go_file(g)
        for fn in funcs:
            content = TEST_TEMPLATE.render(pkg=pkg, func_name=fn)
            fname = out_dir / f"{g.stem}_{fn}_test.go"
            fname.write_text(content)
            count += 1
    return count
