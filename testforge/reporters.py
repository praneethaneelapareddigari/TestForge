def format_summary(coverage_pct: float, mutation_pct: float = None):
    out = f"Coverage: {coverage_pct*100:.2f}%"
    if mutation_pct is not None:
        out += f" — Mutation: {mutation_pct*100:.2f}%"
    return out
