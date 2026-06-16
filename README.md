# Jiading Gai Personal Website

This site uses the MIT-licensed [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme.

## Local Preview

Use Homebrew Ruby on this machine:

```bash
/opt/homebrew/opt/ruby/bin/bundle install
/opt/homebrew/opt/ruby/bin/bundle exec jekyll build
python3 -m http.server 8124 --directory _site
```

Then open <http://127.0.0.1:8124/>.

## Content

- Main profile: `_pages/about.md`
- Publications: `_bibliography/papers.bib`
- Projects: `_projects/`
- Patents: `_pages/patents.md`
