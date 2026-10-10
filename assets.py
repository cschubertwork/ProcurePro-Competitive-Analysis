#!/usr/bin/env python3
"""Capture and embed the dashboard's visual assets. Standard library only, plus
Google Chrome (driven headless over the DevTools protocol, in a throwaway
profile, so nothing signed-in can appear), curl, and macOS `sips`.

  python3 assets.py capture <slug> <url> [<slug> <url> ...]
      Per company: a 16:10 homepage screenshot at 1200px wide (consent banners
      dismissed, lazy images loaded, blocked and broken pages rejected), logo
      candidates, and brand signals read from the rendered page (colours used
      on actions and headers, near-blacks, fonts, theme-color). Writes
      assets/<slug>/, merges into assets/manifest.json after each company, and
      renders every logo candidate on white and near-black into
      assets/logos.png so you can see what the page will actually draw.

  python3 assets.py exhibit <name> <url> <top> <height> [<left> <width>]
      A region of the page at a 1440px viewport, below the fold if need be
      (design doc 8.3: aspect between 16:10 and 3:1), saved as
      assets/exhibits/<name>.jpg at 1200px wide.

  python3 assets.py font "<css2 family spec>" [...]
      e.g. "Figtree:wght@400..800" "IBM+Plex+Mono:wght@400;500". Downloads the
      latin woff2 files into assets/fonts/ and prints the @font-face CSS.

  python3 assets.py embed [index.html]
      Rewrites every src/href="assets/..." and url(assets/...) into a data:
      URI so the page is one self-contained file. Run after every build;
      check.py fails if an assets/ reference is left.

assets/ is gitignored: the page carries the embedded copies, and a re-capture
months later should show the sites as they are then.
"""

import base64
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from datetime import date
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
ASSETS = Path("assets")
SHOT_CAP = 180_000  # bytes per screenshot (design doc 8.6)
BLOCKED = re.compile(r"you've been blocked|attention required|just a moment\.\.\.|verify you are human|"
                     r"access denied|request blocked|are you a robot", re.I)
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml",
        ".webp": "image/webp", ".gif": "image/gif", ".woff2": "font/woff2"}

# Clicks the consent button if there is one, then removes whatever fixed overlay
# still covers a quarter of the viewport, so the screenshot shows the site.
DISMISS_JS = r"""(() => {
  const ok = /^(accept|allow|agree|i agree|i accept|got it|ok|okay|dismiss)\b/i;
  let clicked = 0;
  document.querySelectorAll('button, a, [role=button]').forEach(b => {
    const t = (b.innerText || b.getAttribute('aria-label') || '').trim();
    if (ok.test(t) && b.offsetParent !== null) { b.click(); clicked++; }
  });
  return clicked;
})()"""
UNCOVER_JS = r"""(() => {
  document.querySelectorAll('body *').forEach(e => {
    if (getComputedStyle(e).position !== 'fixed') return;
    const r = e.getBoundingClientRect();
    if (r.width * r.height > innerWidth * innerHeight * 0.25) e.remove();
  });
  document.documentElement.style.overflow = 'auto';
  document.body.style.overflow = 'auto';
})()"""
SCROLL_JS = "(async () => { for (let y = 0; y < document.body.scrollHeight && y < 12000; y += 600) { " \
            "scrollTo(0, y); await new Promise(r => setTimeout(r, 150)); } scrollTo(0, 0); })()"
BROKEN_JS = "[...document.images].filter(i => { const r = i.getBoundingClientRect(); " \
            "return r.top < innerHeight && r.bottom > 0 && r.width > 40 && i.complete && i.naturalWidth === 0; }).length"
BRAND_JS = r"""(() => {
  const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.top < innerHeight * 1.5; };
  const cs = e => getComputedStyle(e);
  const count = {};
  const add = (c, w) => { if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') count[c] = (count[c] || 0) + w; };
  document.querySelectorAll('a, button, [role=button]').forEach(e => { if (vis(e)) { add(cs(e).backgroundColor, 3); add(cs(e).color, 1); } });
  document.querySelectorAll('body, header, nav, footer, h1, h2').forEach(e => { if (vis(e) || e.tagName === 'FOOTER') { add(cs(e).backgroundColor, 2); add(cs(e).color, 1); } });
  const h = document.querySelector('h1, h2');
  const logos = [];
  const sel = 'header a[href="/"], a[href="' + location.origin + '/"], [class*="logo" i], [id*="logo" i], [aria-label*="logo" i]';
  const banner = document.querySelector('header, [role=banner], nav');
  [...(banner ? [banner] : []), ...document.querySelectorAll(sel)].forEach(e => {
    const svg = e.tagName === 'svg' ? e : e.querySelector('svg');
    const img = e.tagName === 'IMG' ? e : e.querySelector('img');
    if (svg && vis(svg)) logos.push({kind: 'svg', html: svg.outerHTML, colour: cs(svg).color});
    if (img && vis(img) && img.currentSrc && !img.currentSrc.startsWith('data:')) logos.push({kind: 'img', src: img.currentSrc});
  });
  const icons = [...document.querySelectorAll('link[rel*=icon]')]
    .map(l => ({apple: l.rel.includes('apple'), size: parseInt(l.sizes.value) || 0, href: l.href}))
    .sort((a, b) => (b.apple - a.apple) || (b.size - a.size));
  return JSON.stringify({
    colours: Object.entries(count).sort((a, b) => b[1] - a[1]).map(([c]) => c),
    fonts: {body: cs(document.body).fontFamily, heading: h ? cs(h).fontFamily : null},
    logos: logos.filter((l, i) => logos.findIndex(m => (m.html || m.src) === (l.html || l.src)) === i).slice(0, 4),
    icons: icons.slice(0, 2),
    theme: (document.querySelector('meta[name=theme-color]') || {}).content || null,
    og: (document.querySelector('meta[property="og:image"]') || {}).content || null,
    text: document.title + ' ' + document.body.innerText.slice(0, 3000),
    url: location.href, lang: document.documentElement.lang || null,
  });
})()"""


def fetch(url, timeout=20):
    # curl rather than urllib: it uses the system certificate store, which a
    # python.org Python build does not.
    r = subprocess.run(["curl", "-sSL", "--fail", "--retry", "2", "--max-time", str(timeout), "-A", UA,
                        "-w", "\n%{content_type}", url], capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stderr.decode(errors="replace").strip())
    body, _, ctype = r.stdout.rpartition(b"\n")
    return body, ctype.decode(errors="replace")


class CDP:
    """Just enough of a websocket client to talk to one Chrome tab."""

    def __init__(self, ws_url):
        u = urlparse(ws_url)
        self.sock = socket.create_connection((u.hostname, u.port), timeout=45)
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall((f"GET {u.path} HTTP/1.1\r\nHost: {u.hostname}:{u.port}\r\nUpgrade: websocket\r\n"
                           f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n").encode())
        head = b""
        while b"\r\n\r\n" not in head:
            head += self.sock.recv(1)
        if b" 101 " not in head.split(b"\r\n")[0]:
            raise RuntimeError(f"websocket upgrade refused: {head[:80]!r}")
        self.next_id = 0

    def _exact(self, n):
        buf = b""
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                raise RuntimeError("Chrome closed the connection")
            buf += chunk
        return buf

    def _send(self, text):
        data = text.encode()
        n = len(data)
        head = bytearray([0x81])
        head += bytes([0x80 | n]) if n < 126 else bytes([0x80 | 126]) + n.to_bytes(2, "big")
        mask = os.urandom(4)
        self.sock.sendall(bytes(head) + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def _recv(self):
        msg = b""
        while True:
            b1, b2 = self._exact(2)
            n = b2 & 0x7F
            if n == 126:
                n = int.from_bytes(self._exact(2), "big")
            elif n == 127:
                n = int.from_bytes(self._exact(8), "big")
            msg += self._exact(n)
            if b1 & 0x80:
                return msg

    def call(self, method, **params):
        self.next_id += 1
        self._send(json.dumps({"id": self.next_id, "method": method, "params": params}))
        while True:  # events arrive interleaved; skip them
            m = json.loads(self._recv())
            if m.get("id") == self.next_id:
                if "error" in m:
                    raise RuntimeError(f"{method}: {m['error']}")
                return m.get("result", {})

    def js(self, expr):
        r = self.call("Runtime.evaluate", expression=expr, awaitPromise=True, returnByValue=True)
        return r.get("result", {}).get("value")


class Browser:
    def __enter__(self):
        self.profile = tempfile.mkdtemp(prefix="assets-chrome-")
        self.proc = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                                      "--remote-debugging-port=0", f"--user-data-dir={self.profile}", "about:blank"],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        port_file = Path(self.profile) / "DevToolsActivePort"
        for _ in range(100):
            if port_file.exists() and port_file.read_text().strip():
                break
            time.sleep(0.1)
        port = port_file.read_text().split()[0]
        tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list").read())
        self.tab = CDP(next(t["webSocketDebuggerUrl"] for t in tabs if t["type"] == "page"))
        self.tab.call("Network.setUserAgentOverride", userAgent=UA)
        return self.tab

    def __exit__(self, *exc):
        self.proc.terminate()
        shutil.rmtree(self.profile, ignore_errors=True)


def load(tab, url, height=900, settle=2.0):
    tab.call("Emulation.setDeviceMetricsOverride", width=1440, height=height, deviceScaleFactor=1, mobile=False)
    tab.call("Page.navigate", url=url)
    deadline = time.time() + 20
    while time.time() < deadline and tab.js("document.readyState") != "complete":
        time.sleep(0.5)
    # A capture taken before the webfonts load shows the site in Times, which misrepresents it.
    tab.js("document.fonts.ready.then(() => document.fonts.status)")
    time.sleep(0.5 + settle)
    if tab.js(DISMISS_JS):
        time.sleep(1.5)
    tab.js(UNCOVER_JS)
    tab.js(SCROLL_JS)
    time.sleep(settle)


def shoot(tab, out, top=0, height=900, left=0, width=1440):
    """A region of the 1440px-wide page rendered 1200px wide (sharper, not blurrier, for narrow
    crops), stepped down in quality to fit the cap."""
    clip = {"x": left, "y": top, "width": width, "height": height, "scale": 1200 / width}
    for q in (72, 64, 56, 48):
        data = base64.b64decode(tab.call("Page.captureScreenshot", format="jpeg", quality=q, clip=clip,
                                         captureBeyondViewport=top + height > 900)["data"])
        if len(data) <= SHOT_CAP:
            break
    out.write_bytes(data)
    return len(data)


def parse_colour(rgb):
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?", rgb)
    if not m or (m.group(4) and float(m.group(4)) < 0.5):
        return None
    return tuple(int(m.group(i)) for i in (1, 2, 3))


def save(url, dest_stem):
    data, ctype = fetch(url)
    ext = Path(urlparse(url).path).suffix.lower()
    if ext not in MIME:
        ext = next((e for k, e in (("svg", ".svg"), ("png", ".png"), ("jpeg", ".jpg"), ("webp", ".webp"))
                    if k in ctype), ".ico")
    out = dest_stem.with_suffix(ext)
    out.write_bytes(data)
    if ext != ".svg":  # png at most 256px: sharp at tile size, light on the page
        png = out.with_suffix(".png")
        subprocess.run(["sips", "-Z", "256", "-s", "format", "png", str(out), "--out", str(png)],
                       capture_output=True)
        if png.exists() and png != out:
            out.unlink()
            out = png
    return out


def capture(tab, slug, url):
    d = ASSETS / slug
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    entry = {"url": url, "captured": date.today().isoformat(), "notes": []}

    for attempt, settle in enumerate((2.0, 4.0)):
        load(tab, url, settle=settle)
        brand = json.loads(tab.js(BRAND_JS))
        blocked = len(brand["text"]) < 200 or BLOCKED.search(brand["text"])
        broken = tab.js(BROKEN_JS)
        if not blocked and not broken:
            break
    entry.update(url_captured=brand["url"], lang=brand["lang"])
    if blocked:
        entry["shot"] = {"status": "unavailable", "reason": "the site blocked automated access"}
        entry["notes"].append("BLOCKED twice; use the fallback frame, or capture by hand in an isolated "
                              "browser (never a signed-in one) and save as home.jpg")
        return entry
    size = shoot(tab, d / "home.jpg")
    entry["shot"] = {"file": f"assets/{slug}/home.jpg", "status": "ok", "bytes": size}
    if broken:
        entry["shot"]["notes"] = f"{broken} image(s) in view still broken after a slower retry; look before using"
        entry["notes"].append(entry["shot"]["notes"])

    chromatic, near_black = [], []
    for c in brand["colours"]:
        rgb = parse_colour(c)
        if not rgb:
            continue
        h = "#%02x%02x%02x" % rgb
        if max(rgb) - min(rgb) >= 24:
            chromatic.append(h)
        elif max(rgb) <= 48:
            near_black.append(h)
    entry.update(theme_color=brand["theme"], colours=list(dict.fromkeys(chromatic))[:8],
                 near_blacks=list(dict.fromkeys(near_black))[:3], fonts=brand["fonts"])

    logos = []
    for i, lg in enumerate(brand["logos"]):
        try:
            if lg["kind"] == "svg":
                svg = lg["html"]
                if "xmlns=" not in svg.split(">", 1)[0]:
                    svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
                # currentColor resolves against the page; pin it so the file renders standalone
                svg = svg.replace("<svg", f'<svg style="color:{lg["colour"]}"', 1)
                p = d / f"logo-{i}.svg"
                p.write_text(svg, encoding="utf-8")
                logos.append(p.as_posix())
            else:
                logos.append(save(lg["src"], d / f"logo-{i}").as_posix())
        except Exception as e:
            entry["notes"].append(f"logo {i}: {e}")
    extra = [("icon", ic["href"]) for ic in brand["icons"]]
    if brand["og"]:
        extra.append(("og-image", urljoin(url, brand["og"])))
    for kind, src in extra:
        try:
            logos.append(save(src, d / kind).as_posix())
        except Exception as e:
            entry["notes"].append(f"{kind}: {e}")
    entry["logo_candidates"] = logos
    return entry


def logo_sheet(tab, manifest):
    """Every candidate drawn through <img> on white and near-black, the way the page will draw it."""
    rows = []
    for slug, e in manifest.items():
        cells = "".join(f'<figure><div class="w"><img src="{Path(p).relative_to(ASSETS)}"></div>'
                        f'<div class="k"><img src="{Path(p).relative_to(ASSETS)}"></div>'
                        f'<figcaption>{Path(p).name}</figcaption></figure>' for p in e.get("logo_candidates", []))
        rows.append(f"<section><h2>{slug}</h2>{cells or '<p>no candidates</p>'}</section>")
    sheet = ASSETS / "logos.html"
    sheet.write_text("<style>body{font:12px system-ui;margin:12px}section{display:flex;gap:10px;align-items:start;"
                     "border-top:1px solid #ccc;padding:8px 0}h2{width:90px;font-size:13px}figure{margin:0}"
                     ".w,.k{width:96px;height:96px;display:grid;place-items:center}.w{background:#fff;outline:1px solid #ddd}"
                     ".k{background:#141414}img{max-width:80px;max-height:80px}</style>" + "".join(rows))
    tab.call("Emulation.setDeviceMetricsOverride", width=1100, height=160 + 230 * len(manifest),
             deviceScaleFactor=1, mobile=False)
    tab.call("Page.navigate", url=sheet.resolve().as_uri())
    time.sleep(1.5)
    (ASSETS / "logos.png").write_bytes(base64.b64decode(tab.call("Page.captureScreenshot", format="png")["data"]))


def cmd_capture(args):
    if not args or len(args) % 2:
        sys.exit("usage: assets.py capture <slug> <url> [<slug> <url> ...]")
    ASSETS.mkdir(exist_ok=True)
    mf = ASSETS / "manifest.json"
    manifest = json.loads(mf.read_text()) if mf.exists() else {}
    with Browser() as tab:
        for slug, url in zip(args[::2], args[1::2]):
            print(f"capturing {slug} ({url})")
            try:
                manifest[slug] = capture(tab, slug, url)
            except Exception as e:
                manifest[slug] = {"url": url, "notes": [f"capture failed: {e}"]}
            for n in manifest[slug]["notes"]:
                print(f"  note: {n}")
            mf.write_text(json.dumps(manifest, indent=2))
        logo_sheet(tab, manifest)
    print(f"wrote {mf} and assets/logos.png. Look at every screenshot and at logos.png before choosing anything.")


def cmd_exhibit(args):
    if len(args) not in (4, 6):
        sys.exit("usage: assets.py exhibit <name> <url> <top> <height> [<left> <width>]")
    name, url = args[0], args[1]
    top, height, left, width = (int(a) for a in (args[2:] + ["0", "1440"])[:4])
    out = ASSETS / "exhibits"
    out.mkdir(parents=True, exist_ok=True)
    with Browser() as tab:
        load(tab, url, height=top + height)
        size = shoot(tab, out / f"{name}.jpg", top=top, height=height, left=left, width=width)
    print(f"wrote {out / name}.jpg ({size // 1024} KB); crop x{left}+{width} y{top}+{height} of {url}")


def cmd_font(args):
    if not args:
        sys.exit('usage: assets.py font "Figtree:wght@400..800" ["IBM+Plex+Mono:wght@400;500" ...]')
    out = ASSETS / "fonts"
    out.mkdir(parents=True, exist_ok=True)
    css_out, seen = [], {}
    for spec in args:
        css = fetch(f"https://fonts.googleapis.com/css2?family={spec.replace(' ', '+')}&display=swap")[0].decode()
        # One block per unicode subset and weight; keep latin, and fetch each file once (variable fonts
        # serve the same file for every weight).
        for block in re.findall(r"/\* latin \*/\s*(@font-face\s*{[^}]+})", css):
            src = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
            family = re.search(r"font-family:\s*'([^']+)'", block).group(1)
            weight = re.search(r"font-weight:\s*([\d ]+);", block).group(1).strip()
            style = re.search(r"font-style:\s*(\w+)", block).group(1)
            key = (src, style)
            if key in seen:
                seen[key]["weights"].append(weight)
                continue
            dest = out / f"{family.replace(' ', '')}-{style}-{len(seen)}.woff2"
            dest.write_bytes(fetch(src)[0])
            urange = re.search(r"unicode-range:\s*([^;]+);", block).group(1)
            seen[key] = {"family": family, "style": style, "file": dest.as_posix(), "weights": [weight], "range": urange}
            print(f"wrote {dest} ({dest.stat().st_size // 1024} KB)", file=sys.stderr)
    for f in seen.values():
        ws = sorted({int(x) for w in f["weights"] for x in w.split()})
        weight = str(ws[0]) if len(ws) == 1 else f"{ws[0]} {ws[-1]}"
        css_out.append(f"@font-face{{font-family:'{f['family']}';font-style:{f['style']};font-weight:{weight};"
                       f"font-display:swap;src:url(\"{f['file']}\") format('woff2');unicode-range:{f['range']}}}")
    print("\n".join(css_out))


def cmd_embed(args):
    page = Path(args[0] if args else "index.html")
    root = (page.parent / "assets").resolve()
    html = page.read_text(encoding="utf-8")

    def data_uri(rel):
        p = (page.parent / rel).resolve()
        if not p.is_relative_to(root) or p.suffix.lower() not in MIME:
            sys.exit(f"refusing to embed {rel}: only image and font files under assets/")
        if not p.exists():
            sys.exit(f"missing asset referenced by {page}: {rel}")
        if p.suffix == ".svg":  # svg stays text: smaller than base64. Quotes are encoded, so it is safe in "..."
            return "data:image/svg+xml," + quote(p.read_text(encoding="utf-8"), safe=" =:/;,")
        return f"data:{MIME[p.suffix.lower()]};base64," + base64.b64encode(p.read_bytes()).decode()

    html = re.sub(r"""((?:src|href)=)(["'])(assets/[^"']+)\2""",
                  lambda m: f'{m.group(1)}"{data_uri(m.group(3))}"', html)
    html = re.sub(r"""url\(\s*(["']?)(assets/[^)"']+)\1\s*\)""", lambda m: f'url("{data_uri(m.group(2))}")', html)
    page.write_text(html, encoding="utf-8")
    print(f"embedded; {page} is now {page.stat().st_size / 1_000_000:.2f} MB")


if __name__ == "__main__":
    cmds = {"capture": cmd_capture, "exhibit": cmd_exhibit, "font": cmd_font, "embed": cmd_embed}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmds[sys.argv[1]](sys.argv[2:])
