#!/usr/bin/env python3
"""
GGC 10K executive network: offline CSV normalization, qualification and approval queues.

No network calls. Does not send messages. All CSV inputs/outputs can contain
private business contact details: keep them OUTSIDE this public repository.
Python 3.10+; standard library only.

Example:
 python scripts/bd_source_graph_v1.py \
   --companies /private/company_master.csv \
   --people /private/people.csv \
   --ledger /private/contact_history.csv \
   --output /private/bd_qa

Companies CSV columns:
 company_id,company_name,parent_company,company_type,owned_product,
 chinese_led,sector,product,scale_evidence,source_url
People CSV columns:
 company_id,name,title,route,route_type,route_verified,role_verified,source_url
Ledger CSV columns:
 company_id,name,event,confirmed,ts
   event in {FIRST_TOUCH, HUMAN_REPLY, HARD_BOUNCE, STOP, OPT_OUT}
Optional STOP CSV:
 company_id,scope,reason
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ACCEPTED_ROUTES = {"direct_business", "official_business", "warm_intro", "business_wechat"}
REJECTED_TYPES = {
    "service_vendor", "marketing_agency", "ua_vendor", "kol_agency",
    "outsourcing_only", "media", "event", "investment_fund",
    "payment_provider", "technology_vendor", "platform_only"
}
PERSON_ROLES = re.compile(
    r"(founder|co.?founder|chief executive|ceo|chair(man|woman|person)?|"
    r"president|gm\b|general manager|studio head|bu head|managing director|"
    r"publishing|commercial|business head|coo|cmo|vice president|vp\b|"
    r"产品负责人|创始人|联合创始人|董事长|总裁|总经理|工作室负责人|"
    r"发行负责人|副总裁|首席运营官|产品总监|运营总监|商业化负责人)",
    re.I,
)
DO_NOT_CONTACT = re.compile(
    r"(游族(网络)?|yoozoo|网龙网络|福建网龙|netdragon)",
    re.I,
)

def norm(value: str) -> str:
    s = unicodedata.normalize("NFKC", value or "").casefold().strip()
    return re.sub(r"[\s\-_,，\.。·•'\"（）()]","",s)

def truth(value: str) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y", "verified"}

def read_csv(path: str | None) -> list[dict]:
    if not path:
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def canonical_company(row: dict) -> str:
    return norm(row.get("parent_company") or row.get("company_name") or row.get("company_id",""))

def company_safe(row: dict) -> tuple[bool, str]:
    combined = " ".join(
        str(row.get(k,"")) for k in ("company_name","parent_company")
    )
    if DO_NOT_CONTACT.search(combined):
        return False, "BANNED_GROUP"
    if norm(row.get("company_type")) in {norm(t) for t in REJECTED_TYPES}:
        return False, "EXCLUDED_THIRD_PARTY"
    if not truth(row.get("chinese_led")):
        return False, "CHINESE_LED_UNVERIFIED"
    if not truth(row.get("owned_product")):
        return False, "OWN_PRODUCT_UNVERIFIED"
    if not row.get("source_url"):
        return False, "SOURCE_REQUIRED"
    return True, "RESEARCH_ELIGIBLE"

def person_safe(row: dict) -> tuple[bool, str]:
    if not row.get("name") or not row.get("title"):
        return False, "MISSING_NAME_OR_TITLE"
    if not PERSON_ROLES.search(row.get("title","")):
        return False, "NOT_CORE_EXECUTIVE"
    if not truth(row.get("role_verified")):
        return False, "ROLE_UNVERIFIED"
    return True, "NAMED_EXECUTIVE"

def route_safe(row: dict) -> tuple[bool, str]:
    rt = (row.get("route_type") or "").strip().lower()
    route = (row.get("route") or "").strip()
    if rt not in ACCEPTED_ROUTES or not truth(row.get("route_verified")):
        return False, "UNVERIFIED_ROUTE"
    if not route:
        return False, "MISSING_ROUTE"
    if re.search(r"(^|@)(support|help|privacy|legal|press|hr|jobs|careers)@",route,re.I):
        return False, "INVALID_FUNCTIONAL_MAILBOX"
    if "@" in route and re.match(r"^(info|hello|contact|service)@", route, re.I):
        return False, "GENERIC_INBOX_NOT_DIRECT"
    return True, "VALID_ROUTE"

def run(args):
    companies=read_csv(args.companies)
    people=read_csv(args.people)
    ledger=read_csv(args.ledger)
    stop=read_csv(args.stop)
    output=Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    company_by_id={}
    canonical={}
    for c in companies:
        cid=str(c.get("company_id","")).strip()
        key=canonical_company(c)
        if not cid or not key:
            continue
        company_by_id[cid]=key
        if key not in canonical:
            canonical[key]=dict(c)
        else:
            # Prefer a row containing stronger scale evidence.
            if len(c.get("scale_evidence","")) > len(canonical[key].get("scale_evidence","")):
                canonical[key]=dict(c)

    company_stop=set()
    person_stop=set()
    hard_bounce=set()
    first_touched=set()
    last_events=defaultdict(list)
    for row in stop:
        k=company_by_id.get(row.get("company_id",""),norm(row.get("company_id","")))
        if (row.get("scope") or "").lower()=="company":
            company_stop.add(k)
        elif (row.get("scope") or "").lower()=="person":
            person_stop.add((k,norm(row.get("name",""))))
    for e in ledger:
        k=company_by_id.get(str(e.get("company_id","")).strip(),"")
        p=norm(e.get("name",""))
        event=str(e.get("event","")).upper().strip()
        if not k:
            continue
        if event in {"STOP", "OPT_OUT"}:
            company_stop.add(k)
        if event == "HARD_BOUNCE":
            hard_bounce.add((k,p))
        if event == "FIRST_TOUCH" and truth(e.get("confirmed")):
            first_touched.add((k,p))
        if event in {"FIRST_TOUCH","HUMAN_REPLY"}:
            last_events[k].append((e.get("ts",""),event))

    company_hold=set()
    company_engaged=set()
    for key,history in last_events.items():
        history=sorted(history)
        if not any(event=="FIRST_TOUCH" for _,event in history):
            continue
        if history and history[-1][1]=="HUMAN_REPLY":
            company_engaged.add(key)
        else:
            company_hold.add(key)

    mapped=defaultdict(list)
    for p in people:
        key=company_by_id.get(str(p.get("company_id","")).strip())
        if not key:
            continue
        mapped[key].append(p)

    counter=Counter()
    approvals=[]
    enrich=[]
    person_seen=set()
    for key,c in sorted(canonical.items()):
        counter["raw_canonical_companies"]+=1
        ok,reason=company_safe(c)
        if not ok:
            counter[reason]+=1
            continue
        counter["eligible_own_product_companies"]+=1
        core=[]
        for p in mapped[key]:
            ok,pr=person_safe(p)
            if not ok:
                continue
            pk=(key,norm(p["name"]))
            if pk in person_seen:
                continue
            person_seen.add(pk)
            core.append(p)
            counter["verified_unique_executives"]+=1
        if len(core)<3:
            counter["company_graph_under_3"]+=1
        if len(core)>=3:
            counter["company_graph_3plus"]+=1
        if key in company_stop:
            counter["company_stop"]+=1
            continue
        if key in company_engaged:
            # Route into Reply Desk / opportunity. Not net-new cold outreach.
            counter["engaged_company_not_new_cold_outreach"]+=1
            continue
        if key in company_hold:
            counter["company_no_reply_hold"]+=1
            continue
        valid=0
        for p in core:
            pk=(key,norm(p["name"]))
            if pk in first_touched:
                counter["already_first_touched_people"]+=1
                continue
            if pk in hard_bounce or pk in person_stop:
                continue
            yes,why=route_safe(p)
            if not yes:
                continue
            valid+=1
            approvals.append({
                "canonical_company":c.get("parent_company") or c.get("company_name"),
                "company_name":c.get("company_name"),
                "name":p.get("name"),
                "title":p.get("title"),
                "route":p.get("route"),
                "route_type":p.get("route_type"),
                "company_source":c.get("source_url"),
                "person_source":p.get("source_url"),
                "evidence":c.get("scale_evidence"),
                "status":"NEEDS_JOYCE_COMPANY_PERSON_COPY_APPROVAL"
            })
        if valid:
            counter["untouched_contact_ready_companies"]+=1
            counter["new_valid_person_routes"]+=valid
        else:
            enrich.append({
                "company":c.get("company_name"),
                "named_core_people":len(core),
                "reason":"NO_VALID_UNTOUCHED_EXECUTIVE_ROUTE"
            })

    counter["confirmed_unique_first_touches_total_in_ledger"]=len(first_touched)
    counter["confirmed_unique_first_touches_eligible_subset"] = sum(
        1 for k,p in first_touched if k in canonical and company_safe(canonical[k])[0]
    )
    counter["target_remaining_eligible_unique_people"]=max(
        0,10000-counter["confirmed_unique_first_touches_eligible_subset"]
    )
    counter["approval_pending_people"]=len(approvals)

    def export_csv(name, rows, fields):
        with (output/name).open("w",newline="",encoding="utf-8-sig") as f:
            w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)

    export_csv("approval_queue.csv",approvals,[
        "canonical_company","company_name","name","title","route","route_type",
        "company_source","person_source","evidence","status"
    ])
    export_csv("needs_enrichment.csv",enrich,[
        "company","named_core_people","reason"
    ])
    with (output/"metrics.json").open("w",encoding="utf-8") as f:
        json.dump(dict(counter),f,ensure_ascii=False,indent=2,sort_keys=True)
    print(json.dumps(dict(counter),ensure_ascii=False,indent=2,sort_keys=True))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--companies",required=True)
    parser.add_argument("--people",required=True)
    parser.add_argument("--ledger",required=True)
    parser.add_argument("--stop")
    parser.add_argument("--output",required=True)
    run(parser.parse_args())
