"""Convert Markdown files to standalone HTML next to each source file.

Usage: python -I md_to_html.py <repo_root> <file.md> [<file.md> ...]
Relative links to .md files are rewritten to .html.
"""
import html
import re
import sys
from pathlib import Path

import markdown

CSS = """
:root { --bg:#ffffff; --fg:#1f2328; --muted:#59636e; --border:#d1d9e0; --code:#f6f8fa; --link:#0969da; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#0d1117; --fg:#e6edf3; --muted:#9198a1; --border:#3d444d; --code:#151b23; --link:#4493f8; }
}
html { background: var(--bg); }
body { background: var(--bg); color: var(--fg); margin: 0 auto; max-width: 980px; padding: 32px 16px 64px;
  font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
a { color: var(--link); }
h1, h2 { border-bottom: 1px solid var(--border); padding-bottom: .3em; }
code, pre { background: var(--code); border-radius: 6px; font: 85% ui-monospace, SFMono-Regular, Consolas, monospace; }
code { padding: .2em .4em; }
pre { padding: 16px; overflow-x: auto; }
pre code { padding: 0; background: none; }
table { border-collapse: collapse; display: block; overflow-x: auto; margin: 16px 0; }
th, td { border: 1px solid var(--border); padding: 6px 13px; vertical-align: top; }
th { background: var(--code); }
blockquote { margin: 0; padding: 0 1em; color: var(--muted); border-left: .25em solid var(--border); }
img { max-width: 100%; }
hr { border: 0; border-top: 1px solid var(--border); }
"""

LINK_RE = re.compile(r'href="(?!https?:|mailto:|#)([^"#]+)\.md(#[^"]*)?"')


def convert(path: Path) -> Path:
    text = path.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "toc"])
    body = LINK_RE.sub(lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', body)
    heading = re.search(r"^#\s+(.+)$", text, re.M)
    title = heading.group(1).strip() if heading else path.stem
    out = path.with_suffix(".html")
    out.write_text(
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{html.escape(title)}</title>\n<style>{CSS}</style>\n</head>\n"
        f"<body>\n{body}\n</body>\n</html>\n",
        encoding="utf-8",
        newline="\n",
    )
    return out


if __name__ == "__main__":
    root = Path(sys.argv[1])
    for name in sys.argv[2:]:
        print(convert(root / name).relative_to(root))
