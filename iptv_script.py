import requests

# ====================== 【你只需要改这里】 ======================

# 远程直播源地址
REMOTE_URL = "https://freetv.fun/test_channels_original_new.txt?key=1831"

# 固定保留的源
RESERVE = """
广东卫视,https://example.com/gdtv.m3u8
湖南卫视,https://example.com/hunan.m3u8
"""

# 黑名单（频道名包含这些就过滤）
EXCLUDE = """
测试
垃圾
广告
"""

# 频道分类
CHANNEL_GROUPS = {
    "央视频道,#genre#": ["CCTV1", "CCTV2", "CCTV3", "CCTV4", "CCTV5", "CCTV5+"],
    "广东频道,#genre#": ["广东卫视", "广州", "深圳", "汕头", "佛山"],
    "卫视频道,#genre#": ["湖南", "浙江", "北京", "江苏", "上海", "东方"],
    "港澳频道,#genre#": ["TVB", "凤凰", "澳视", "星空"],
}

# 输出文件名
OUTPUT_TXT = "iptv4.txt"
OUTPUT_M3U = "iptv4.m3u"

# ====================== 下面不用动 ======================

def clean(s):
    s = s.strip()
    for ch in "[]()HDBDSD4K1080p720p-_ |":
        s = s.replace(ch, "")
    return s

# 下载源
resp = requests.get(REMOTE_URL, timeout=15)
lines = resp.text.splitlines()

# 加载保留、黑名单
reserve_lines = [l.strip() for l in RESERVE.splitlines() if l.strip()]
exclude_set = {clean(l) for l in EXCLUDE.splitlines() if l.strip()}

# 合并所有频道
all_channels = []
for line in lines + reserve_lines:
    line = line.strip()
    if "," not in line:
        continue
    name, url = line.split(",", 1)
    cname = clean(name)
    if any(ex in cname for ex in exclude_set):
        continue
    all_channels.append((cname, name, url))

# 去重
all_channels = list(dict.fromkeys(all_channels))

# 生成 txt
txt = ""
for group, keys in CHANNEL_GROUPS.items():
    txt += group + "\n"
    for cname, name, url in all_channels:
        if any(k in cname for k in keys):
            txt += f"{name},{url}\n"

# 生成 m3u
m3u = "#EXTM3U\n"
for group, keys in CHANNEL_GROUPS.items():
    gtitle = group.split(",")[0]
    for cname, name, url in all_channels:
        if any(k in cname for k in keys):
            m3u += f'#EXTINF:-1 tvg-name="{name}" group-title="{gtitle}",{name}\n{url}\n'

# 写入文件
with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
    f.write(txt)
with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
    f.write(m3u)

print("✅ 生成完成：", OUTPUT_TXT, OUTPUT_M3U)

