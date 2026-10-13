#!/usr/bin/env python3
"""Read-only public inventory. No DNS/login changes, no paid content, no form POST.
Only hosts literally present in repository text + known GGC hosts + explicit proposals.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode, urlsplit
from html import unescape
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import argparse, json, re, unicodedata
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
DATA=json.loads((HERE/'catalog.json').read_text(encoding='utf-8'))
UA={'User-Agent':'GGC-Public-Link-Review/1.0 (read-only)'}
def text_title(raw):
    match=re.search(r'<title[^>]*>(.*?)</title>',raw,re.S|re.I)
    return unescape(re.sub(r'\s+',' ',match.group(1))).strip() if match else ''
def get(url,limit=400000):
    try:
        with urlopen(Request(url,headers=UA),timeout=12) as r:
            data=r.read(limit);html=data.decode('utf-8','replace')
            return {'url':url,'final_url':r.url,'status':r.status,'title':text_title(html),'server':r.headers.get('Server'),'html':html}
    except Exception as err:return {'url':url,'error':type(err).__name__+': '+str(err)[:180]}
def norm(v):return ''.join(unicodedata.normalize('NFKC',v).split()).casefold()
def course(c):
    result=get('https://www.sanjieke.cn/course/detail/sjk/'+c['id']);html=result.pop('html','')
    title=result.get('title','');result.update(id=c['id'],expected_title=c['title'],metadata_matches=norm(c['title']) in norm(title) and 'joyce' in norm(title))
    result['classification']='matched_public_metadata' if result['metadata_matches'] else 'needs_manual_review_not_proof_of_deletion'
    return result

def host(record):
    name,sources=record;result={'host':name,'source_files':sources[:4]}
    for kind in ['A','CNAME']:
        response=get('https://dns.google/resolve?'+urlencode({'name':name,'type':kind}),70000)
        if 'html' in response:
            try:
                j=json.loads(response['html']);result[kind]={'status':j.get('Status'),'answers':[a.get('data') for a in j.get('Answer',[])]}
            except Exception:result[kind]={'error':'DNS response was not JSON'}
        else:result[kind]={'error':response.get('error')}
    if result.get('A',{}).get('status')==0 and result.get('A',{}).get('answers'):
        response=get('https://'+name+'/',100000);response.pop('html',None);result['http']=response
    return result

def run(out):
    out.mkdir(parents=True,exist_ok=True)
    found={n:['known_existing_reference'] for n in ['ggcgames.com','www.ggcgames.com','biz.ggcgames.com','opsgo.ggcgames.com']}
    for f in REPO.rglob('*'):
        if not f.is_file() or '.git' in f.parts or f.suffix not in ['.md','.html','.js','.py','.json','.yml','.yaml','.txt'] or f.stat().st_size>2000000:continue
        if any(x in f.parts for x in ['academy-evidence','fullsite-evidence','p0-evidence']):continue
        for n in set(re.findall(r'(?<![\w-])(?:[a-zA-Z0-9][a-zA-Z0-9-]*\.)+ggcgames\.com\b',f.read_text(errors='ignore'))):
            found.setdefault(n.lower(),[]).append(str(f.relative_to(REPO)))
    found.setdefault('academy.ggcgames.com',['proposal_only_not_assumed_existing'])
    records=sorted(found.items())[:50]
    with ThreadPoolExecutor(max_workers=4) as pool:domains=list(pool.map(host,records))
    with ThreadPoolExecutor(max_workers=3) as pool:courses=list(pool.map(course,DATA['courses']+DATA['hold']))
    report={'checked_at':datetime.now(timezone.utc).isoformat(),'scope':'Public DNS/HTTP and repository-mentioned hosts; NOT an authoritative Alibaba DNS-zone inventory. Successful HTTP alone is not product, privacy or payment acceptance.','domain_candidates_total':len(found),'domain_limit':50,'truncated':len(found)>50,'domains':domains,'courses':courses,'production_changed':False,'video_accessed':False}
    (out/'public-inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PUBLIC_DOMAIN_AUDIT '+json.dumps(domains,ensure_ascii=False))
    print('PUBLIC_COURSE_AUDIT '+json.dumps(courses,ensure_ascii=False))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.out)
