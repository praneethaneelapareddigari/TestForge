import subprocess
from pathlib import Path

def run_python_mutation(target: Path):
    # requires mutmut installed (pip install mutmut)
    return subprocess.run(["mutmut", "run", "--paths", str(target)], capture_output=True, text=True)

def run_java_mutation(target: Path):
    # expects Maven + PIT plugin configured in project POM
    return subprocess.run(["mvn", "org.pitest:pitest-maven:mutationCoverage"], cwd=str(target), capture_output=True, text=True)

def run_go_mutation(target: Path):
    # expects go-mutesting installed
    return subprocess.run(["go-mutesting", "./..."], cwd=str(target), capture_output=True, text=True)

def run_ts_mutation(target: Path):
    # expects stryker (npm) configured
    return subprocess.run(["npx", "stryker", "run"], cwd=str(target), capture_output=True, text=True)
