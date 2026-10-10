"""Derive the per-run colour tokens for a landscape dashboard from one brand colour.

Usage: python3 derive_tokens.py '#593CFB' [--dark '#121214'] [--css]
Prints a contrast report; with --css, prints the paste-ready token blocks instead. Stdlib only.
Every text pairing it emits is >= 4.5:1 and every solid mark >= 3:1 (highlighter mode excepted:
there the brand fill sits behind ink and every filled mark takes a 1px --ink outline).
"""
import math, sys

# ---------- colour maths (OKLab / OKLCH, sRGB) ----------
def hex_to_rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#' + ''.join(f'{round(max(0, min(1, c)) * 255):02X}' for c in rgb)

def to_lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def from_lin(c): return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

def rgb_to_oklch(rgb):
    r, g, b = (to_lin(c) for c in rgb)
    l = 0.4122214708*r + 0.5363325363*g + 0.0514459929*b
    m = 0.2119034982*r + 0.6806995451*g + 0.1073969566*b
    s = 0.0883024619*r + 0.2817188376*g + 0.6299787005*b
    l, m, s = (x ** (1/3) for x in (l, m, s))
    L = 0.2104542553*l + 0.7936177850*m - 0.0040720468*s
    a = 1.9779984951*l - 2.4285922050*m + 0.4505937099*s
    bb = 0.0259040371*l + 0.7827717662*m - 0.8086757660*s
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360

def oklch_to_rgb_raw(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l = (L + 0.3963377774*a + 0.2158037573*b) ** 3
    m = (L - 0.1055613458*a - 0.0638541728*b) ** 3
    s = (L - 0.0894841775*a - 1.2914855480*b) ** 3
    r = 4.0767416621*l - 3.3077115913*m + 0.2309699292*s
    g = -1.2684380046*l + 2.6097574011*m - 0.3413193965*s
    bl = -0.0041960863*l - 0.7034186147*m + 1.7076147010*s
    return tuple(from_lin(c) if c >= 0 else -from_lin(-c) for c in (r, g, bl))

def in_gamut(rgb): return all(-1e-4 <= c <= 1 + 1e-4 for c in rgb)

def oklch(L, C, H):
    """OKLCH to hex, reducing chroma until it fits sRGB (keeps L and H)."""
    lo, hi = 0.0, C
    if in_gamut(oklch_to_rgb_raw(L, C, H)): return rgb_to_hex(oklch_to_rgb_raw(L, C, H))
    for _ in range(30):
        mid = (lo + hi) / 2
        if in_gamut(oklch_to_rgb_raw(L, mid, H)): lo = mid
        else: hi = mid
    return rgb_to_hex(oklch_to_rgb_raw(L, lo, H))

def lum(hx):
    r, g, b = (to_lin(c) for c in hex_to_rgb(hx)); return 0.2126*r + 0.7152*g + 0.0722*b

def cr(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)

# ---------- derivation ----------
ALERT_H = 28  # fixed alert hue (red-orange)

def neutrals(H, C_scale, dark_seed=None):
    n = lambda L, C: oklch(L, C * C_scale, H)
    light = dict(bg=n(.985, .006), surface=n(.998, .003), surface2=n(.955, .010),
                 rule=n(.905, .012), rulestrong=n(.835, .014),
                 ink3=n(.525, .016), ink2=n(.415, .018), ink=n(.215, .020))
    if dark_seed:
        L0, _, _ = rgb_to_oklch(hex_to_rgb(dark_seed)); L0 = min(max(L0, .15), .21)
    else:
        L0 = .170
    dark = dict(bg=dark_seed or n(L0, .010), surface=n(L0 + .040, .012), surface2=n(L0 + .070, .014),
                rule=n(L0 + .130, .014), rulestrong=n(L0 + .210, .016),
                ink3=n(.700, .014), ink2=n(.800, .012), ink=n(.950, .008))
    return light, dark

def step_to_contrast(L, C, H, grounds, target, direction):
    """Move L in `direction` (-1 darker, +1 lighter) until contrast >= target on every ground."""
    for _ in range(100):
        hx = oklch(L, C, H)
        if min(cr(hx, g) for g in grounds) >= target: return hx, L
        L += 0.005 * direction
        if not 0 <= L <= 1: break
    return oklch(L, C, H), L

def derive(brand, dark_seed=None):
    Lb, Cb, Hb = rgb_to_oklch(hex_to_rgb(brand))
    achromatic = Cb < 0.04
    H = 250 if achromatic else Hb
    C_scale = 0.6 if achromatic else 1.0
    light, dark = neutrals(H, C_scale, dark_seed)
    out = {'light': light, 'dark': dark, 'notes': []}
    if achromatic:
        out['notes'].append('Achromatic brand: neutral-accent mode (accent = ink, target marked by weight and solid ink fill).')
    for theme, t, direction in (('light', light, -1), ('dark', dark, +1)):
        grounds = [t['bg'], t['surface'], t['surface2']]
        if achromatic:
            acc, fill = t['ink'], t['ink']
            mode = 'neutral'
        else:
            acc, La = step_to_contrast(Lb, Cb, H, grounds, 4.5, direction)
            _, Ca_real, _ = rgb_to_oklch(hex_to_rgb(acc))
            recognisable = abs(La - Lb) <= 0.22 and Ca_real >= 0.45 * Cb
            if min(cr(brand, g) for g in grounds) >= 3.0:
                fill = brand                     # the real brand colour carries solid marks
            else:
                fill, _ = step_to_contrast(Lb, Cb, H, grounds, 3.0, direction)
            mode = 'ink' if recognisable else 'highlighter'
            if mode == 'highlighter':
                # Neon or pale brand: brand stays a fill behind ink; text accent becomes ink.
                acc = t['ink']; fill = brand
                out['notes'].append(f'{theme}: brand fails as text without losing its identity; highlighter mode.')
        on = '#FFFFFF' if cr('#FFFFFF', fill) >= cr(t['ink'] if theme == 'light' else light['ink'], fill) else (t['ink'] if theme == 'light' else light['ink'])
        if cr(on, fill) < 4.5 and mode != 'highlighter':
            fill, _ = step_to_contrast(rgb_to_oklch(hex_to_rgb(fill))[0], Cb, H, [on], 4.5, -1 if on == '#FFFFFF' else +1)
        if theme == 'light':
            wash = oklch(.955, min(.045, max(Cb, .02) * .30), H)
            line = oklch(.800, min(.110, max(Cb, .02) * .55), H)
        else:
            wash = oklch(rgb_to_oklch(hex_to_rgb(t['bg']))[0] + .075, min(.060, max(Cb, .02) * .35), H)
            line = oklch(.520, min(.130, max(Cb, .02) * .60), H)
        if achromatic:
            wash, line = t['surface2'], t['rulestrong']
        if mode == 'ink' and cr(acc, wash) < 4.5:   # accent labels also sit on the wash
            acc, _ = step_to_contrast(rgb_to_oklch(hex_to_rgb(acc))[0], Cb, H, grounds + [wash], 4.5, direction)
        t.update(accent=acc, accentfill=fill, onaccent=on, accentwash=wash, accentline=line)
        # alert: fixed hue, falls back to ink-inverse when the brand hue is close
        clash = (not achromatic) and min(abs(Hb - ALERT_H), 360 - abs(Hb - ALERT_H)) < 35
        if clash:
            t.update(alert=t['ink'], alertwash=t['surface2'])
            out['notes'].append(f'{theme}: brand hue within 35deg of alert; alert chips use ink-inverse.')
        else:
            aw = oklch(.950 if theme == 'light' else rgb_to_oklch(hex_to_rgb(t['bg']))[0] + .07, .035 if theme == 'light' else .05, ALERT_H)
            a, _ = step_to_contrast(.56 if theme == 'light' else .74, .19 if theme == 'light' else .15, ALERT_H, grounds + [aw], 4.5, direction)
            t.update(alert=a, alertwash=aw)
        t['_mode'] = mode
    out['brand'] = brand; out['oklch'] = (round(Lb, 3), round(Cb, 3), round(Hb, 1))
    return out

def report(d):
    print(f"brand {d['brand']}  oklch {d['oklch']}")
    for n in d['notes']: print('  note:', n)
    for theme in ('light', 'dark'):
        t = d[theme]
        print(f"  [{theme}] mode={t['_mode']}")
        print('   ', '  '.join(f"{k}={v}" for k, v in t.items() if not k.startswith('_')))
        chk = [('ink/bg', t['ink'], t['bg']), ('ink2/bg', t['ink2'], t['bg']), ('ink3/bg', t['ink3'], t['bg']),
               ('ink3/surface2', t['ink3'], t['surface2']), ('accent/bg', t['accent'], t['bg']),
               ('accent/surface2', t['accent'], t['surface2']), ('accentfill/bg', t['accentfill'], t['bg']),
               ('onaccent/fill', t['onaccent'], t['accentfill']), ('ink/wash', t['ink'], t['accentwash']),
               ('ink2/wash', t['ink2'], t['accentwash']), ('accent/wash', t['accent'], t['accentwash']), ('alert/bg', t['alert'], t['bg']),
               ('alert/alertwash', t['alert'], t['alertwash']), ('rulestrong/bg', t['rulestrong'], t['bg'])]
        print('   ', '  '.join(f"{n}={cr(a, b):.2f}" for n, a, b in chk))

NAMES = [('bg','--bg'),('surface','--surface'),('surface2','--surface-2'),('rule','--rule'),
         ('rulestrong','--rule-strong'),('ink','--ink'),('ink2','--ink-2'),('ink3','--ink-3'),
         ('accent','--accent'),('accentfill','--accent-fill'),('onaccent','--on-accent'),
         ('accentwash','--accent-wash'),('accentline','--accent-line'),('alert','--alert'),('alertwash','--alert-wash')]

def css(d):
    blk = lambda t: '\n'.join(f'  {css_name}: {t[k]};' for k, css_name in NAMES)
    L, D = d['light'], d['dark']
    print(f"/* tokens derived from {d['brand']} (oklch {d['oklch']}); light mode={L['_mode']}, dark mode={D['_mode']} */")
    print(':root {\n  color-scheme: light;\n' + blk(L) + f"\n  --accent-mode: {L['_mode']};\n}}")
    print('@media (prefers-color-scheme: dark) {\n  :root:not([data-theme="light"]) {\n    color-scheme: dark;\n' + blk(D).replace('\n  ', '\n    ').replace('  --', '    --', 1) + f"\n    --accent-mode: {D['_mode']};\n  }}\n}}")
    print(':root[data-theme="dark"] {\n  color-scheme: dark;\n' + blk(D) + f"\n  --accent-mode: {D['_mode']};\n}}")

if __name__ == '__main__':
    args = sys.argv[1:]
    dark = None
    if '--dark' in args:
        i = args.index('--dark'); dark = args[i + 1]; del args[i:i + 2]
    as_css = '--css' in args
    args = [a for a in args if a != '--css']
    for b in args: (css if as_css else report)(derive(b, dark))
