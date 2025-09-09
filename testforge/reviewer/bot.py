import requests
from typing import Optional

GITHUB_API = "https://api.github.com"

def post_review_comment(repo_full_name: str, pr_number: int, token: str, body: Optional[str] = None) -> bool:
    """
    Post a simple comment to the PR summarizing coverage status.
    repo_full_name: e.g. "org/repo"
    pr_number: PR id
    token: GitHub token with repo:status or repo access
    """
    if body is None:
        # attempt to read coverage.xml and create a short summary
        cov = "coverage.xml not found"
        try:
            with open("coverage.xml") as fh:
                txt = fh.read()
                if 'line-rate="' in txt:
                    rate = float(txt.split('line-rate="')[1].split('"')[0])
                    cov = f"Coverage: {rate*100:.2f}%"
        except Exception:
            pass
        body = f"TestForge automated review — {cov}"

    url = f"{GITHUB_API}/repos/{repo_full_name}/issues/{pr_number}/comments"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    resp = requests.post(url, json={"body": body}, headers=headers)
    return resp.status_code in (200, 201)
