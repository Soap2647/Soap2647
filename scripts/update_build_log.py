"""Writes the latest ai-build-log entries into README.md between the BUILD-LOG markers."""
import json
import os
import re
import urllib.request

REPO = "Soap2647/ai-build-log"
COUNT = 5
START, END = "<!-- BUILD-LOG:START -->", "<!-- BUILD-LOG:END -->"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-build-log"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


tree = json.loads(get(f"https://api.github.com/repos/{REPO}/git/trees/main?recursive=1"))["tree"]
paths = sorted((t["path"] for t in tree if re.fullmatch(r"log/\d{4}/\d{4}-\d{2}-\d{2}\.md", t["path"])), reverse=True)

rows = []
for path in paths[:COUNT]:
    text = get(f"https://raw.githubusercontent.com/{REPO}/main/{path}")
    date = path[-13:-3]
    title = next((l[2:].split("·", 1)[-1].strip() for l in text.splitlines() if l.startswith("# ")), date)
    summary = next((l[1:].strip() for l in text.splitlines() if l.startswith(">")), "")
    rows.append(f"| `{date}` | [**{title}**](https://github.com/{REPO}/blob/main/{path})<br/><sub>{summary}</sub> |")

block = "\n".join([START, "", "| Day | What I built with AI |", "|---|---|", *rows, "", END])
readme = open("README.md", encoding="utf-8").read()
new = re.sub(re.escape(START) + ".*?" + re.escape(END), lambda _: block, readme, flags=re.S)
if new != readme:
    open("README.md", "w", encoding="utf-8").write(new)
    print(f"updated with {len(rows)} entries")
else:
    print("no change")
