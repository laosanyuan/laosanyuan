import base64, json, os, sys, urllib.request
from pathlib import Path

API = "https://wakatime.com/api/v1/users/current/stats/last_7_days"
START = "<!--START_SECTION:waka-->"
END = "<!--END_SECTION:waka-->"
README = Path(__file__).resolve().parent.parent / "README.md"

def trim_right(s, n):
    return s if len(s) <= n else s[: n - 3] + "..."

def bar_chart(percent, size=21):
    syms = "░▏▎▍▌▋▊▉█"
    frac = int((size * 8 * percent) // 100)
    full = frac // 8
    if full >= size:
        return syms[8] * size
    semi = frac % 8
    return (syms[8] * full + syms[semi]).ljust(size, syms[0])

def fetch_stats(key):
    auth = base64.b64encode((key + ":").encode()).decode()
    req = urllib.request.Request(API, headers={"Authorization": "Basic " + auth, "User-Agent": "readme-wakatime"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def body_for(stats):
    langs = (stats.get("data") or {}).get("languages") or []
    if not langs:
        return "最近 7 天没有记录到编码时间。"
    lines = []
    for item in langs[:5]:
        name = trim_right(item["name"], 10).ljust(10)
        tm = item["text"].ljust(14)
        pct = f"{item['percent']:5.1f}%"
        lines.append(f"{name} {tm} {bar_chart(item['percent'])} {pct}")
    return "\n".join(lines)

def main():
    key = os.environ.get("WAKATIME_API_KEY", "").strip()
    if not key:
        sys.exit("缺少 WAKATIME_API_KEY secret")
    try:
        stats = fetch_stats(key)
    except Exception as e:
        sys.exit(f"WakaTime 请求失败: {e}")

    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        sys.exit("README 缺少 WakaTime 区块标记")
    block = f"{START}\n```text\n{body_for(stats)}\n```\n{END}"
    new = text.split(START)[0] + block + text.split(END)[1]
    if new == text:
        print("无变化")
        return
    README.write_text(new, encoding="utf-8")
    print("已更新")

if __name__ == "__main__":
    main()
