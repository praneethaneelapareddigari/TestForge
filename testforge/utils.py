from pathlib import Path

def detect_languages(path: Path):
    langs = set()
    for p in path.rglob('*'):
        if p.suffix == '.py':
            langs.add('python')
        if p.suffix == '.java':
            langs.add('java')
        if p.suffix == '.go':
            langs.add('go')
        if p.suffix in ('.ts', '.js', '.tsx', '.jsx'):
            langs.add('ts')
    return sorted(langs)
