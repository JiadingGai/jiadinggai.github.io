# Jiading Gai Personal Website

This branch uses jemdoc-style source files and committed static HTML output.
GitHub Pages should serve the branch directly as plain files; `.nojekyll`
disables Jekyll processing.

## Publishing

Use GitHub Pages with:

- Source: `Deploy from a branch`
- Branch: `jemdoc-devel` for preview, or `main` after merge
- Folder: `/ (root)`

## Content

- Source files: `jemdoc/*.jemdoc`
- Menu: `jemdoc/MENU`
- jemdoc configuration: `jemdoc/site.conf`
- Stylesheet: `assets/css/jemdoc.css`
- Generated pages: `index.html`, `publications/index.html`,
  `projects/index.html`, `patents/index.html`, `blog/index.html`

## Rebuild

Install or download `jemdoc+MathJax` from
`https://github.com/wsshin/jemdoc_mathjax`, then run:

```bash
JEMDOC=/path/to/jemdoc python3 tools/build_jemdoc_site.py
```

Recent Python versions may print upstream `SyntaxWarning` messages while
running `jemdoc+MathJax`; the build is valid as long as the command exits
successfully.
