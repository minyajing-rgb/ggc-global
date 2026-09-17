#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bd_pipeline.py · 百万年框BD全链路自动化 v1.0 (2026-09-17)
链路: sourcing(画像筛选) → pitch(母版装配) → 跟进(+5/+10天自动排队) → 达成(meeting brief)
用法:
  python3 bd_pipeline.py --stage sourcing --scan <每日扫描json>   # ①筛目标
  python3 bd_pipeline.py --stage pitch --company <名> --data <json> # ②装配pitch
  python3 bd_pipeline.py --stage followup                        # ③跟进队列
  python3 bd_pipeline.py --stage funnel                          # ④漏斗报告
  python3 bd_pipeline.py --stage all --scan <json>                # 全链路
状态源: /app/drafts/bd_crm_ledger.json (主库快照, 每次操作后同步GitHub bd/crm/)
"""
import json, os, sys, argparse, subprocess
from datetime import datetime, timedelta

LEDGER = "/app/drafts/bd_crm_ledger.json"
TG = "/app/tg_send.py"

# 百万年框画像 (LOCKED 2026-09-17)
PROFILE = {
    "pool_B_high_value": ["publisher","ceo_founder","casino","sims","ai_native","investor","strategic_partner","early_stage"],
    "pool_A_scale": ["hybrid_casual","puzzle","merge","idle","arcade","mobile_studio"],
    "thresholds": {"min_monthly_rev_usd": 3000000, "takeoff_window_months": 6,
                   "signals": ["recent_funding","chart_breakout","no_global_ops"]}
}
FOLLOWUP_DAYS = {"first": 5, "final": 10}

def load_ledger():
    if os.path.exists(LEDGER):
        return json.load(open(LEDGER))
    return {"companies": []}

def save_ledger(led):
    json.dump(led, open(LEDGER, "w"), ensure_ascii=False, indent=1)

def cmd_sourcing(scan_file):
    """①sourcing: 按画像过滤扫描候选, 输出入池建议 + ownership判定"""
    scan = json.load(open(scan_file))
    led = load_ledger()
    owned = [c["company"].lower() for c in led["companies"]]
    out = []
    for cand in scan.get("candidates", []):
        name = cand.get("company","").lower()
        if name in owned:
            out.append((cand.get("company"), "SKIP-已入池(ownership保护)")); continue
        fit, reasons = 0, []
        rev = cand.get("monthly_rev_usd", 0)
        if rev >= PROFILE["thresholds"]["min_monthly_rev_usd"]: fit += 2; reasons.append(f"月流水${rev/1e6:.1f}M")
        for s in cand.get("signals", []):
            if s in PROFILE["thresholds"]["signals"]: fit += 1; reasons.append(s)
        cat = cand.get("category","")
        pool = "B(GGC助理)" if any(k in cat for k in PROFILE["pool_B_high_value"]) else "A(Codex)" if any(k in cat for k in PROFILE["pool_A_scale"]) else "?"
        grade = "HIGH" if fit >= 3 else "MEDIUM" if fit == 2 else "LOW"
        out.append((cand.get("company"), f"{grade} | pool={pool} | {', '.join(reasons) if reasons else '信号不足'}"))
    report = "🎯 <b>BD Sourcing队列</b>\n" + "\n".join(f"• <b>{n}</b>: {r}" for n, r in out)
    subprocess.run(["python3", TG, report])
    return out

def cmd_pitch(company, data_file):
    """②pitch: 从10版母版装配定制pitch(A/B轮转), 输出邮件草稿"""
    data = json.load(open(data_file))
    led = load_ledger()
    variants = [c.get("variant","B") for c in led["companies"] if c.get("category")==data.get("category")]
    variant = "A" if variants.count("B") > variants.count("A") else "B"  # 自动平衡A/B
    template = data["template_slots"]  # {hook_numbers, founder_name, email}
    pitch = data["master"].replace("[硬数字]", template["hook_numbers"]).replace("[Name]", template["founder_name"])
    draft_path = f"/tmp/pitch_{company.replace(' ','_')}.md"
    open(draft_path, "w").write(f"Subject: {data['subject']}\n\n{pitch}")
    return draft_path, variant

def cmd_followup():
    """③followup: 扫描ledger, 首发无回复+5天→第一封跟进, +10天→最后一封"""
    led = load_ledger(); today = datetime.now()
    due = []
    for c in led["companies"]:
        fs = c.get("first_sent"); rt = c.get("reply_type", "")
        if not fs or rt in ("Positive","Neutral"): continue
        d = datetime.fromisoformat(fs[:10])
        if (today - d).days >= FOLLOWUP_DAYS["final"] and not c.get("final_sent"):
            due.append((c["company"], "FINAL-最后一封(窗口期收尾)"))
        elif (today - d).days >= FOLLOWUP_DAYS["first"] and not c.get("followup_sent"):
            due.append((c["company"], "FOLLOWUP-1(新硬数字钩子跟进)"))
    if due:
        subprocess.run(["python3", TG, "📮 <b>BD跟进队列(自动)</b>\n" + "\n".join(f"• {n}: {t}" for n, t in due)])
    return due

def cmd_funnel():
    """④funnel: 漏斗+A/B对比, Meeting Rate为北极星"""
    led = load_ledger(); cs = led["companies"]
    stats = {}
    for c in cs:
        v = c.get("variant","-"); stats.setdefault(v, dict(total=0, replied=0, positive=0, meeting=0))
        s = stats[v]; s["total"] += 1
        if c.get("reply_type") in ("Positive","Neutral"): s["replied"] += 1
        if c.get("reply_type") == "Positive": s["positive"] += 1
        if c.get("meeting") == "Yes": s["meeting"] += 1
    lines = [f"📊 <b>BD漏斗报告</b> · 北极星=Meeting Rate", ""]
    for v, s in sorted(stats.items()):
        rr = s["replied"]/s["total"]*100 if s["total"] else 0
        mr = s["meeting"]/s["total"]*100 if s["total"] else 0
        lines.append(f"Variant {v}: {s['total']}封 | 回复率{rr:.0f}% | Positive {s['positive']} | <b>Meeting {s['meeting']} ({mr:.0f}%)</b>")
    lines.append(f"\n池内公司总数: {len(cs)}")
    subprocess.run(["python3", TG, "\n".join(lines)])
    return stats

def cmd_meeting_brief(company):
    """达成段: Positive回复→自动出meeting brief框架, GGC助理填产品数据后发Joyce"""
    brief = f"""📋 Meeting Brief · {company}
1. 对方产品硬数据(榜单/收入/融资, GGC助理核实后填)
2. 判断的3个结构性问题(钩子)
3. 合作切入角度(CP/Publisher/Startup/Investor/AI选类)
4. 可能异议+回应锚点(¥10K Project Review → Sprint → 年框)
5. 下一步承诺(时间/方式)"""
    open(f"/tmp/brief_{company.replace(' ','_')}.md", "w").write(brief)
    return f"/tmp/brief_{company.replace(' ','_')}.md"

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--stage", required=True, choices=["sourcing","pitch","followup","funnel","brief","all"])
    p.add_argument("--scan"); p.add_argument("--company"); p.add_argument("--data")
    a = p.parse_args()
    if a.stage in ("sourcing","all") and a.scan: cmd_sourcing(a.scan)
    if a.stage == "pitch" and a.company and a.data:
        path, v = cmd_pitch(a.company, a.data); print(f"✅ pitch草稿: {path} (variant={v})")
    if a.stage in ("followup","all"): print(f"跟进队列: {cmd_followup()}")
    if a.stage in ("funnel","all"): print(f"漏斗: {cmd_funnel()}")
    if a.stage == "brief" and a.company: print(f"✅ {cmd_meeting_brief(a.company)}")
