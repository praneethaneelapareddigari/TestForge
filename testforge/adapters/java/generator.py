import re
from pathlib import Path
from jinja2 import Template

# Simple JUnit 5 class template (assumes package statement if present)
CLASS_TEMPLATE = Template("""\
package {{ package }};

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class {{ class_name }}Test {

    @Test
    public void {{ method_name }}_smoke() {
        {{ class_name }} inst = new {{ class_name }}();
        // TODO: replace with meaningful assertions
        assertNotNull(inst);
    }
}
""")

def parse_java_file(path: Path):
    text = path.read_text()
    pkg = ""
    m = re.search(r'^\s*package\s+([\\w\\.]+);', text, re.MULTILINE)
    if m:
        pkg = m.group(1)
    classes = re.findall(r'public\s+class\s+([A-Z][A-Za-z0-9_]*)', text)
    return pkg, classes

def generate_tests_for_target(target: Path):
    target = Path(target)
    out_dir = target / "tests_generated" / "java"
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for j in target.rglob("*.java"):
        pkg, classes = parse_java_file(j)
        for cls in classes:
            # pick a default method name
            method = "smoke"
            package_decl = pkg if pkg else "generated"
            content = CLASS_TEMPLATE.render(package=package_decl, class_name=cls, method_name=method)
            # create path mapping package -> dirs
            pkg_path = package_decl.replace(".", "/")
            target_dir = out_dir / pkg_path
            target_dir.mkdir(parents=True, exist_ok=True)
            fname = target_dir / f"{cls}Test.java"
            fname.write_text(content)
            count += 1
    return count
