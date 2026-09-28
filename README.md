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

## Google Search

The build generates page-specific descriptions and canonical HTTPS URLs, plus
`sitemap.xml` for the seven content pages. `robots.txt` allows crawling and points
to the sitemap. The 404 page is excluded from the sitemap and marked `noindex`.
Commit the rebuilt HTML and sitemap with source changes before publishing.

To check actual Google indexing:

1. Open [Google Search Console](https://search.google.com/search-console) and add
   the URL-prefix property `https://jiadinggai.github.io/`.
2. Verify ownership with Google's HTML-file method: place the exact downloaded
   verification file at the repository root, commit and publish it, then click
   Verify. Keep the file published after verification. Do not add it to the sitemap.
3. Under Sitemaps, submit `https://jiadinggai.github.io/sitemap.xml`.
4. Use URL Inspection on `https://jiadinggai.github.io/`, check the live URL, and
   request indexing if needed. Repeat for important new or updated pages.
5. Check the Page indexing report for crawl failures or excluded pages.

Public access and a sitemap do not prove a page is indexed. Google decides
whether and when to include pages; crawling can take days to weeks. See Google's
[recrawl guidance](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl)
and [ownership verification guide](https://support.google.com/webmasters/answer/9008080).
