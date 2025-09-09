import yaml
from pathlib import Path
def load_config(path: Path = Path("testforge.config.yaml")):
    p = Path(path)
    if p.exists():
        return yaml.safe_load(p.read_text())
    return {}
