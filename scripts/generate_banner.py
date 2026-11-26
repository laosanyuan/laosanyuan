import base64, re, subprocess
from pathlib import Path

ICON_NAMES = ["csharp","dotnet","flutter","dart","python","typescript","vuedotjs","git","redis","github"]
LAYOUT = {
    "csharp": (830,180,64), "dotnet": (1080,100,48), "flutter": (950,105,58),
    "dart": (735,100,46), "python": (1030,255,56), "typescript": (910,275,44),
    "vuedotjs": (790,260,52), "git": (870,80,40), "redis": (1120,195,48),
    "github": (960,190,40),
}
UA = {"User-Agent": "profile-banner-generator"}

def fetch(url: str) -> bytes:
    return subprocess.check_output(["curl", "-sSL", "--fail", "--max-time", "30", url])

def icon_path(name: str) -> str:
    svg = fetch(f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{name}.svg")
    return re.search(rb'<path d="([^"]+)"', svg).group(1).decode()

def build(theme: dict, avatar_b64: str, paths: dict) -> str:
    icons = []
    for name, (cx, cy, size) in LAYOUT.items():
        s = size / 24
        icons.append(
            f'<g transform="translate({cx - size/2} {cy - size/2}) '
            f'scale({s:.4f})" opacity="0.92"><path d="{paths[name]}" '
            f'fill="{theme["ink"]}"/></g>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-labelledby="title desc"><title id="title">一刀</title><desc id="desc">个人主页横幅：头像、名字、技术栈图标</desc><defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="0.7" fill="{theme['grid']}" opacity="0.8"/></pattern><clipPath id="avatar"><circle cx="154" cy="182" r="86"/></clipPath></defs><rect width="1200" height="360" fill="{theme['bg']}"/><rect width="1200" height="360" fill="url(#grid)"/>{''.join(icons)}<circle cx="161" cy="191" r="88" fill="{theme['accent']}" opacity="0.22"/><circle cx="154" cy="182" r="94" fill="{theme['bg']}"/><image x="68" y="96" width="172" height="172" preserveAspectRatio="xMidYMid slice" clip-path="url(#avatar)" xlink:href="data:image/jpeg;base64,{avatar_b64}"/><circle cx="154" cy="182" r="94" fill="none" stroke="{theme['ink']}" stroke-width="2"/><text x="277" y="193" font-family="'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif" font-size="86" font-weight="700" letter-spacing="6" fill="{theme['accent']}" opacity="0.22">一刀</text><text x="272" y="188" font-family="'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif" font-size="86" font-weight="700" letter-spacing="6" fill="{theme['ink']}">一刀</text><text x="276" y="232" font-family="system-ui, -apple-system, 'Segoe UI', sans-serif" font-size="21" font-weight="400" letter-spacing="1" fill="{theme['muted']}">C# / .NET · Flutter · Rust · Python</text><text x="276" y="272" font-family="system-ui, -apple-system, 'Segoe UI', sans-serif" font-size="11" font-weight="500" letter-spacing="1.6" fill="{theme['meta']}">HANGZHOU · yhonglai@163.com</text><line x1="276" y1="302" x2="700" y2="302" stroke="{theme['line']}" stroke-width="1"/></svg>'''

light = dict(bg="#F5F0E7", grid="#E8E0D3", accent="#D23A2A", ink="#161616", muted="#6E655A", meta="#8E8578", line="#D8CFC0")
dark = dict(bg="#101012", grid="#1D1D20", accent="#E4503A", ink="#F3EEE5", muted="#A69C90", meta="#7E766C", line="#2B2A2C")

paths = {n: icon_path(n) for n in ICON_NAMES}
avatar = base64.b64encode(fetch("https://avatars.githubusercontent.com/u/18140832?s=120")).decode()

out = Path(__file__).resolve().parent.parent / "assets"
out.mkdir(exist_ok=True)
(out / "banner-light.svg").write_text(build(light, avatar, paths), encoding="utf-8")
(out / "banner-dark.svg").write_text(build(dark, avatar, paths), encoding="utf-8")
print("generated", (out / "banner-light.svg").stat().st_size, (out / "banner-dark.svg").stat().st_size)
