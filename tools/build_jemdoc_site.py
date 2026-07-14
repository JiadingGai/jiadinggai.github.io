#!/usr/bin/env python3
"""Build committed HTML pages from jemdoc sources.

Set JEMDOC=/path/to/jemdoc to use a local jemdoc+MathJax checkout.
The generated HTML is committed so GitHub Pages can serve this branch as
plain static files.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JEMDOC = os.environ.get("JEMDOC", "jemdoc")
CONF = ROOT / "jemdoc" / "site.conf"
SITE_URL = "https://jiadinggai.github.io"

PAGES = [
    ("jemdoc/index.jemdoc", "index.html"),
    ("jemdoc/publications.jemdoc", "publications/index.html"),
    ("jemdoc/projects.jemdoc", "projects/index.html"),
    ("jemdoc/patents.jemdoc", "patents/index.html"),
    ("jemdoc/blog.jemdoc", "blog/index.html"),
    ("jemdoc/bpftrace-uprobe-stack.jemdoc", "blog/2026/bpftrace-uprobe-stack/index.html"),
    ("jemdoc/mytransformers.jemdoc", "blog/2026/mytransformers/index.html"),
    ("jemdoc/404.jemdoc", "404.html"),
]

ACTIVE_LINK = {
    "index.html": "index.html",
    "publications/index.html": "../publications/index.html",
    "projects/index.html": "../projects/index.html",
    "patents/index.html": "../patents/index.html",
    "blog/index.html": "../blog/index.html",
    "blog/2026/bpftrace-uprobe-stack/index.html": "../../../blog/index.html",
    "blog/2026/mytransformers/index.html": "../../../blog/index.html",
    "404.html": "404.html",
}


def postprocess_html(path: Path, output: str) -> None:
    html = path.read_text()
    html = html.replace('target=&ldquo;blank&rdquo;', 'target="_blank"')
    html = html.replace('target="blank"', 'target="_blank"')
    html = re.sub(r'(<a href="(?!https?://)[^"]+") target="_blank"', r"\1", html)
    html = html.replace(' class="current"', "")
    active = ACTIVE_LINK.get(output)
    if active:
        html = html.replace(f'<a href="{active}">', f'<a href="{active}" class="current">', 1)
    path.write_text(html)


def write_sitemap() -> None:
    urls = []
    for _, output in PAGES:
        if output == "404.html":
            continue
        suffix = "" if output == "index.html" else output.removesuffix("index.html")
        urls.append(f"{SITE_URL}/{suffix}")

    entries = "\n".join(f"  <url><loc>{url}</loc></url>" for url in urls)
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(sitemap)


def main() -> int:
    env = os.environ.copy()
    env.setdefault("PYTHONWARNINGS", "ignore::SyntaxWarning")
    for source, output in PAGES:
        output_path = ROOT / output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        jemdoc_cmd = [JEMDOC]
        if os.path.exists(JEMDOC):
            jemdoc_cmd = [sys.executable, JEMDOC]
        cmd = jemdoc_cmd + ["-c", str(CONF), "-o", str(output_path), str(ROOT / source)]
        print(" ".join(cmd))
        subprocess.run(cmd, cwd=ROOT, check=True, env=env)
        postprocess_html(output_path, output)
    write_sitemap()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
