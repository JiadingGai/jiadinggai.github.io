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
from html import escape
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


PAGE_DESCRIPTIONS = {
    "index.html": (
        "Jiading Gai's research, publications, and technical notes on GPU systems, CUDA kernels, "
        "compiler engineering, and efficient machine learning."
    ),
    "publications/index.html": (
        "Research publications by Jiading Gai and coauthors on GPU systems, "
        "machine learning, reinforcement learning, and high-performance computing."
    ),
    "projects/index.html": (
        "Jiading Gai's research projects: F2Asm NVIDIA SASS encoders, DualKV FlashAttention, "
        "CUDA kernel optimization, and IMPATIENT MRI."
    ),
    "patents/index.html": "Patents and patent applications coauthored by Jiading Gai.",
    "blog/index.html": (
        "Technical articles by Jiading Gai on GPU systems, native function tracing, "
        "and Transformer machine translation."
    ),
    "blog/2026/bpftrace-uprobe-stack/index.html": (
        "Confirm native function calls with bpftrace uprobes, process filtering, "
        "call counts, and user-space stack traces, using DualKV as an example."
    ),
    "blog/2026/mytransformers/index.html": (
        "Transformer machine translation in PyTorch: attention, encoder-decoder interaction, "
        "training, and BLEU, with equations and code."
    ),
    "404.html": "The requested page could not be found on Jiading Gai's website.",
}


def canonical_url(output: str) -> str:
    return f"{SITE_URL}/{output.removesuffix('index.html')}"


def postprocess_html(path: Path, output: str) -> None:
    html = path.read_text()
    marker = "<!-- SEARCH_METADATA -->"
    if html.count(marker) != 1:
        raise ValueError(f"Expected one search metadata placeholder in {output}")
    metadata = f'<meta name="description" content="{escape(PAGE_DESCRIPTIONS[output])}" />'
    if output == "404.html":
        metadata += '\n<meta name="robots" content="noindex" />'
    else:
        metadata += f'\n<link rel="canonical" href="{escape(canonical_url(output))}" />'
    html = html.replace(marker, metadata)
    if output != "index.html":
        html = re.sub(r"(<title>.*?)(</title>)", r"\1 | Jiading Gai\2", html, count=1)
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
        urls.append(canonical_url(output))

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
