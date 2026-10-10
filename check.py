#!/usr/bin/env python3
"""Publish gate for an employer-facing competitive-analysis repo.

Deny-by-default: every file that would ship must be on the allowlist below,
and shipped content must pass the scans. Run from the repo root, or pass the
root as the only argument. Exit 0 = clean, 1 = findings.

To extend the layout, edit ALLOWED_FILES / ALLOWED_DIR_PREFIXES here and
nowhere else. Adding a path to the gate is a reviewed edit, not a flag.
"""

import re
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path

ALLOWED_FILES = {
    "README.md",
    "index.html",
    ".nojekyll",
    ".gitignore",
    "check.py",
    "CLAUDE.md",
    "assets.py",
    "derive_tokens.py",
}
ALLOWED_DIR_PREFIXES = (
    "reference/",
    "profiles/",
    "analysis/",
    "templates/",
    ".claude/skills/",
)
REQUIRED_FILES = ("README.md", "index.html", ".nojekyll", ".gitignore")

# Templates ship placeholders on purpose, and skills quote them as instructions.
PLACEHOLDER_EXEMPT = ("templates/", ".claude/skills/")

SECRET_PATTERNS = [
    (re.compile(r"\bghp_[A-Za-z0-9]{20,}"), "GitHub token"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"), "GitHub fine-grained token"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{24,}"), "API secret key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{35}"), "Google API key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY"), "private key block"),
    (re.compile(r"Authorization:\s*(Bearer|Basic)\s+\S+", re.I), "Authorization header"),
]

EMDASH_PATTERNS = ("—", "&mdash;", "&#8212;", "&#x2014;")

# A caption explains the data; it never talks to the builder (dashboard-design.md 9.8, D4).
BUILD_NOTE_RE = re.compile(r"never alert|monogram tile|now sourced|sits above|per the current profiles", re.I)

EXTERNAL_ASSET_PATTERNS = [
    (re.compile(r"<script[^>]*\ssrc\s*=\s*[\"']?(https?:)?//", re.I), "external script"),
    (re.compile(r"<link[^>]*\shref\s*=\s*[\"']?(https?:)?//", re.I), "external stylesheet/link"),
    (re.compile(r"<img[^>]*\ssrc\s*=\s*[\"']?(https?:)?//", re.I), "external image"),
    (re.compile(r"<iframe[^>]*\ssrc\s*=", re.I), "iframe"),
    (re.compile(r"@import\b", re.I), "CSS @import"),
    (re.compile(r"url\(\s*[\"']?(https?:)?//", re.I), "external url() in CSS"),
    # Anything else that fetches: srcset, poster, <source>, an <image> or <use> inside inline SVG.
    # Links (<a href>) are expected and excluded.
    (re.compile(r"<(?!a\b)[a-z][^>]*\s(?:src|href|xlink:href|srcset|poster|data)\s*=\s*[\"']?(https?:)?//", re.I),
     "external reference"),
]
# A page that still points at assets/ was not run through `assets.py embed`.
UNEMBEDDED_RE = re.compile(r"""(?:src|href|srcset|poster)\s*=\s*["']?assets/|url\(\s*["']?assets/""", re.I)
# Embedded image and font payloads. Base64 has no quotes, spaces, < > or parens, so stripping
# exactly this can never hide prose or markup from the scans, only binary from assets/.
DATA_URI_RE = re.compile(r"data:(?:image/(?:png|jpeg|webp|gif)|font/woff2);base64,[A-Za-z0-9+/]+=*")
PAGE_WARN_BYTES, PAGE_MAX_BYTES = 2_000_000, 2_500_000

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
TODO_RE = re.compile(r"\b(TODO|FIXME)\b")
OBSERVED_RE = re.compile(r"^\s*-\s*Observed:")

findings = []
warnings = []


def fail(path, rule, detail, line=None):
    loc = f"{path}:{line}" if line else str(path)
    findings.append(f"{loc}  [{rule}]  {detail}")


def warn(path, rule, detail, line=None):
    loc = f"{path}:{line}" if line else str(path)
    warnings.append(f"{loc}  [{rule}]  {detail}")


def load_gitignore(root):
    patterns = []
    gi = root / ".gitignore"
    if gi.exists():
        for raw in gi.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw.strip()
            if line and not line.startswith("#"):
                patterns.append(line.rstrip("/"))
    return patterns


def is_ignored(rel, patterns):
    parts = rel.split("/")
    for pat in patterns:
        if "/" in pat:
            # Directory-prefix pattern (e.g. ".claude/agent-memory-local"): matches itself
            # and everything nested under it, not just a single path segment.
            if rel == pat or rel.startswith(pat + "/") or fnmatch(rel, pat):
                return True
        elif any(fnmatch(part, pat) for part in parts):
            return True
    return False


def is_allowed(rel):
    if rel in ALLOWED_FILES:
        return True
    return any(rel.startswith(p) for p in ALLOWED_DIR_PREFIXES)


def shippable_paths(root, patterns):
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if rel.startswith(".git/") or rel == ".git":
            continue
        if is_ignored(rel, patterns):
            continue
        yield rel, p


def check_layout(root, patterns):
    for req in REQUIRED_FILES:
        if not (root / req).exists():
            fail(req, "layout", "required file is missing")
    for rel, _ in shippable_paths(root, patterns):
        if rel.startswith(".claude/") and not rel.startswith(".claude/skills/"):
            fail(rel, "layout", "nothing under .claude/ may ship except .claude/skills/")
        elif not is_allowed(rel):
            fail(rel, "layout", "not on the publish allowlist (edit ALLOWED_* in check.py if this is deliberate)")


def check_gitignore_mode(root):
    gi = root / ".gitignore"
    if not gi.exists():
        return
    text = gi.read_text(encoding="utf-8", errors="replace")
    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    for line in lines:
        if re.match(r"^(profiles|analysis|exports|reference)\b", line):
            fail(".gitignore", "gitignore-mode",
                 f"tracker-mode pattern '{line}' would strip the intelligence out of the published repo")
    if ".claude/agent-memory-local/" not in text:
        fail(".gitignore", "gitignore-mode", "must ignore .claude/agent-memory-local/")


def check_git_tracked(root):
    if not (root / ".git").exists():
        return
    try:
        out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        warn(".git", "git", "could not run git ls-files")
        return
    for rel in out.splitlines():
        if rel.startswith(".claude/") and not rel.startswith(".claude/skills/"):
            fail(rel, "git", "tracked file under .claude/ outside .claude/skills/")
        elif not is_allowed(rel):
            fail(rel, "git", "tracked file not on the publish allowlist")


def scan_text(rel, path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if rel.endswith(".html"):
        text = DATA_URI_RE.sub("data:embedded", text)
    lines = text.splitlines()
    exempt_placeholders = rel.startswith(PLACEHOLDER_EXEMPT)
    for i, line in enumerate(lines, 1):
        for pat, name in SECRET_PATTERNS:
            if pat.search(line):
                fail(rel, "secret", name, i)
        if "/Users/" in line:
            fail(rel, "local-path", "absolute local path", i)
        for dash in EMDASH_PATTERNS:
            if dash in line:
                fail(rel, "em-dash", f"em dash ({dash!r})", i)
        if rel.endswith(".html"):
            m = BUILD_NOTE_RE.search(line)
            if m:
                fail(rel, "caption", f"build note in reader-facing copy ({m.group(0)!r})", i)
        if not exempt_placeholders and PLACEHOLDER_RE.search(line):
            fail(rel, "placeholder", PLACEHOLDER_RE.search(line).group(0), i)
        if not exempt_placeholders and TODO_RE.search(line):
            fail(rel, "todo", TODO_RE.search(line).group(0), i)
        m = EMAIL_RE.search(line)
        if m and "noreply" not in m.group(0) and "example.com" not in m.group(0):
            warn(rel, "email", m.group(0), i)


def check_claims(root, patterns):
    depth_full = []
    for rel, path in shippable_paths(root, patterns):
        if not (rel.startswith(("profiles/", "analysis/")) and rel.endswith(".md")):
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if OBSERVED_RE.match(line) and "http" not in line:
                fail(rel, "attribution", "Observed claim with no URL (label it Inferred or add the source)", i)
        if rel.startswith("profiles/") and "Depth: full" in path.read_text(encoding="utf-8", errors="replace"):
            depth_full.append(rel)
    if depth_full and not (root / "analysis" / "verification-note.md").exists():
        fail("analysis/verification-note.md", "verification",
             f"missing, but deep profiles exist: {', '.join(depth_full)}")


def check_readme(root):
    readme = root / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8", errors="replace")
    if "affiliated" not in text.lower():
        fail("README.md", "readme", "missing the not-affiliated disclaimer")
    if not re.search(r"20\d\d", text):
        fail("README.md", "readme", "missing a produced-on date")


def check_self_contained(root):
    index = root / "index.html"
    if not index.exists():
        return
    text = DATA_URI_RE.sub("data:embedded", index.read_text(encoding="utf-8", errors="replace"))
    for i, line in enumerate(text.splitlines(), 1):
        for pat, name in EXTERNAL_ASSET_PATTERNS:
            if pat.search(line):
                fail("index.html", "self-contained", name, i)
        if UNEMBEDDED_RE.search(line):
            fail("index.html", "self-contained", "references assets/ directly; run `python3 assets.py embed`", i)
    size = index.stat().st_size
    if size > PAGE_MAX_BYTES:
        fail("index.html", "page-weight", f"{size / 1e6:.2f} MB is over the {PAGE_MAX_BYTES / 1e6:.1f} MB limit")
    elif size > PAGE_WARN_BYTES:
        warn("index.html", "page-weight", f"{size / 1e6:.2f} MB is over the {PAGE_WARN_BYTES / 1e6:.1f} MB warning line")


def check_dead_anchors(root):
    """A tab bar sends an unknown hash to tab 1 silently, which hides a dead link that a plain
    page would just fail to jump for. Catch it here instead."""
    index = root / "index.html"
    if not index.exists():
        return
    text = index.read_text(encoding="utf-8", errors="replace")
    ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', text))
    for m in re.finditer(r'href=["\']#([^"\']+)["\']', text):
        target = m.group(1)
        if target and target not in ids:
            fail("index.html", "dead-anchor", f'href="#{target}" has no matching id')


def main():
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    if not root.is_dir():
        print(f"not a directory: {root}")
        return 2
    patterns = load_gitignore(root)
    check_layout(root, patterns)
    check_gitignore_mode(root)
    check_git_tracked(root)
    for rel, path in shippable_paths(root, patterns):
        if rel.endswith((".md", ".html", ".template")):
            scan_text(rel, path)
    check_claims(root, patterns)
    check_readme(root)
    check_self_contained(root)
    check_dead_anchors(root)

    for w in warnings:
        print(f"WARN  {w}")
    if findings:
        for f in findings:
            print(f"FAIL  {f}")
        print(f"\n{len(findings)} finding(s). Fix before publishing.")
        return 1
    print(f"PASS  {root.name} is clean ({len(warnings)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
