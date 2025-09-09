import xml.etree.ElementTree as ET
from pathlib import Path

def parse_cobertura_xml(xml_path: Path):
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    # Cobertura uses 'line-rate' attribute on the root
    lr = root.attrib.get("line-rate")
    if lr:
        return float(lr)
    # some variants store coverage in packages -> package -> line-rate
    for pkg in root.findall(".//package"):
        lr = pkg.attrib.get("line-rate")
        if lr:
            return float(lr)
    return 0.0

def check_coverage(min_threshold: float = 0.92) -> bool:
    cov_file = Path("coverage.xml")
    if not cov_file.exists():
        print("coverage.xml not found; failing gate.")
        return False
    rate = parse_cobertura_xml(cov_file)
    print(f"Detected coverage (line-rate): {rate:.4f}")
    return rate >= min_threshold
