import typer
from pathlib import Path
from testforge.adapters.python.generator import generate_tests_for_target as gen_py
from testforge.adapters.java.generator import generate_tests_for_target as gen_java
from testforge.adapters.go.generator import generate_tests_for_target as gen_go
from testforge.adapters.ts.generator import generate_tests_for_target as gen_ts
from testforge.quality.coverage_gate import check_coverage
from testforge.reviewer.bot import post_review_comment
from testforge.config import load_config

app = typer.Typer(help="TestForge – Multi-language test generator & reviewer")

@app.command()
def bootstrap(target: Path):
    target.mkdir(parents=True, exist_ok=True)
    (target / "tests").mkdir(exist_ok=True)
    (target / "testforge.config.yaml").write_text("min_coverage: 0.92\n")
    typer.echo(f"Bootstrapped {target}")

@app.command()
def generate(lang: str, target: Path):
    """
    lang: one of python|java|go|ts|all
    target: path to repo or package to scan
    """
    t = Path(target)
    total = 0
    if lang in ("python", "all"):
        c = gen_py(t)
        typer.echo(f"Python: generated {c} tests")
        total += c
    if lang in ("java", "all"):
        c = gen_java(t)
        typer.echo(f"Java: generated {c} tests (stubs)")
        total += c
    if lang in ("go", "all"):
        c = gen_go(t)
        typer.echo(f"Go: generated {c} tests (stubs)")
        total += c
    if lang in ("ts", "all"):
        c = gen_ts(t)
        typer.echo(f"TS: generated {c} tests (stubs)")
        total += c
    typer.echo(f"TOTAL generated tests: {total}")

@app.command("quality-gate")
def quality_gate(min: float = 0.92):
    ok = check_coverage(min)
    if ok:
        typer.echo("Coverage gate passed")
        raise typer.Exit(code=0)
    else:
        typer.echo("Coverage gate failed")
        raise typer.Exit(code=2)

@app.command("review")
def review(repo_full_name: str, pr_number: int, token: str = typer.Option(None)):
    """
    Post a lightweight review comment to the PR (needs GITHUB token)
    """
    token_opt = token
    if not token_opt:
        typer.echo("No token provided; skipping review.")
        raise typer.Exit(code=1)
    posted = post_review_comment(repo_full_name, pr_number, token_opt)
    typer.echo("Posted review" if posted else "Failed to post review")
