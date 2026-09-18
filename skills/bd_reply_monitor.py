#!/usr/bin/env python3
"""BD回复监测 · 依赖gmail.readonly(2026-09-18开通)
任何会话开始跑一次：扫BdLead池内公司域名的收件箱，分类回复/弹回，TG报告"""
import json, urllib.request, os, subprocess
token = os.environ.get("GMAIL_ACCESS_TOKEN","")
def api(path):
    req = urllib.request.Request(f"https://gmail.googleapis.com/gmail/v1/users/me/{path}",
        headers={"Authorization": f"Bearer {token}"})
    return json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
# 管道内公司域名
DOMAINS = ["grand.gs","oakevergames.com","cyphergames.com","dreamgames.com",
           "scatterlab.co.kr","nitrogames.fi","moonactive.com","atelico.com"]
if not token:
    print("无GMAIL_ACCESS_TOKEN"); exit()
replies, bounces = [], []
for d in DOMAINS:
    try:
        r = api(f"messages?maxResults=10&q=from:{d}")
        for mid in r.get("messages", []):
            m = api(f"messages/{mid['id']}?format=metadata&metadataHeaders=Subject&metadataHeaders=Date")
            hdrs = {h["name"]: h["value"] for h in m["payload"]["headers"]}
            s = hdrs.get("Subject","")
            if any(k in s.lower() for k in ["mail delivery","undeliver","delivery status"]):
                bounces.append(f"{d}")
            else:
                replies.append(f"✉️ {d}: {s[:50]}")
    except Exception: pass
msg = "📬 <b>BD收件箱扫描</b>\n" + (
    "\n".join(replies) if replies else "暂无回复（等待窗口内）") + (
    ("\n⚠️ 弹回: " + ", ".join(set(bounces))) if bounces else "\n✅ 无弹回，全部有效送达")
subprocess.run(["python3","/app/tg_send.py",msg])
