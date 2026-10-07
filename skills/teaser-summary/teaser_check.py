#!/usr/bin/env python3
"""teaser_check.py — 悬念缺口式摘要校验（结论泄露/伏笔/分层文案/链接白名单）"""
import re, sys

ALLOWED_LINKS = ["tianji.saga1001.com", "bunny.saga1001.com", "opsgo.ggcgames.com", "t.zsxq.com", "ggcgames.com", "saga1001.com"]
LEAK_PATTERNS = [r"结论[是就：:]", r"答案[是就：:]", r"所以应该", r"因此应该", r"正确做法[是：:]", r"最终判断[是：:]"]
FORESHADOW = re.compile(r"(星球|deep dive|deep dive|更深一层|完整deep dive)")
LAYERED_CLOSING = re.compile(r"(只拆到表层|只想要一个简单结论|看到这里就够)")

def check(path):
    text = open(path, encoding="utf-8").read()
    problems = []
    for p in LEAK_PATTERNS:
        m = re.search(p, text)
        if m:
            problems.append(f"结论泄露：命中「{m.group(0)}」——最终判断必须留在星球")
    if len(text) < 800:
        problems.append(f"长度不足：{len(text)}字符（公开摘要仍需实质内容，最低800）")
    if not FORESHADOW.search(text):
        problems.append("缺少伏笔：正文中部需要一次「更深一层在星球deep dive展开」式软伏笔")
    if not LAYERED_CLOSING.search(text):
        problems.append("缺少预期分层固定文案（本篇只拆到表层…/只想要简单结论看到这里就够）")
    ext_links = re.findall(r"https?://([^\s)】」\"]+)", text)
    for l in ext_links:
        if not any(a in l for a in ALLOWED_LINKS):
            problems.append(f"外部链接违规：{l}")
    return problems

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: teaser_check.py <摘要文件>"); sys.exit(1)
    problems = check(sys.argv[1])
    if not problems:
        print("PASS ✓ 悬念缺口式摘要合格，可发布")
        sys.exit(0)
    print("FAIL — 当次修复后再验：")
    for p in problems: print(" •", p)
    sys.exit(1)
