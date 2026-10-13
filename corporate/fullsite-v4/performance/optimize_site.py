"""Conservative post-build optimization of the accepted GGC pages (stdlib only).
Never publishes, requests a font, re-encodes approved images or enables a form.
Original inputs stay byte-identical. Fonts, CSS cascade and deferred JS order stay.
"""
from pathlib import Path
from html import escape, unescape
from html.parser import HTMLParser
from urllib.parse import urlsplit
import argparse, gzip, hashlib, json, re, struct

VERSION = '2026-10-13-product-review-performance-1'
FONT_ORIGIN = 'https://fonts.googleapis.com'
TAG = re.compile(r'<link\b[^>]*>|<script\b[^>]*>\s*</script>|<img\b[^>]*>', re.I)
IMPORT = re.compile(r'@import\s+url\([\"\']?(https://fonts\.googleapis\.com/[^\"\')]+)[\"\']?\)\s*;')

class Attrs(HTMLParser):
    def handle_starttag(self, tag, attrs): self.tag, self.attrs = tag, dict(attrs)

def attrs(text):
    parser = Attrs(); parser.feed(text)
    return parser.tag, parser.attrs

def digest(data): return hashlib.sha256(data).hexdigest()
def gzlen(data): return len(gzip.compress(data, compresslevel=9, mtime=0))

def local_file(site, page, href):
    u = urlsplit(href)
    if u.scheme or u.netloc or u.query or u.fragment: return None
    # Root 404 uses a base directory; use the assets anchor, not the runtime URL.
    if '/assets/' in u.path:
        rel = u.path.split('/assets/', 1)[1]
        p = site/'assets'/rel
    elif u.path.startswith('assets/'):
        p = site/u.path
    else:
        p = (page.parent/u.path).resolve()
    p = p.resolve()
    if not p.is_relative_to((site/'assets').resolve()): return None
    if not p.is_file(): raise ValueError(f'Missing local resource: {href}')
    return p

def without_comments(css):
    """Do not change any whitespace in selectors, values, calc() or strings."""
    out=[]; i=0; quote=None
    while i<len(css):
        c=css[i]
        if quote:
            out.append(c)
            if c=='\\' and i+1<len(css):
                i+=1;out.append(css[i])
            elif c==quote: quote=None
        elif c in ['"', "'"]:
            quote=c;out.append(c)
        elif css.startswith('/*',i):
            end=css.find('*/',i+2)
            if end<0:raise ValueError('Unclosed CSS comment')
            out.append('\n');i=end+1
        else:out.append(c)
        i+=1
    return ''.join(out).strip()

def webp_dimensions(path):
    b=path.read_bytes()
    if b[:4]!=b'RIFF' or b[8:12]!=b'WEBP':raise ValueError('Unexpected image format')
    offset=12
    while offset+8<=len(b):
        name=b[offset:offset+4];n=int.from_bytes(b[offset+4:offset+8],'little');d=b[offset+8:offset+8+n]
        if name==b'VP8X':return 1+int.from_bytes(d[4:7],'little'),1+int.from_bytes(d[7:10],'little')
        if name==b'VP8 ' and len(d)>=10 and d[3:6]==b'\x9d\x01\x2a':
            return int.from_bytes(d[6:8],'little')&16383,int.from_bytes(d[8:10],'little')&16383
        if name==b'VP8L' and len(d)>=5 and d[0]==47:
            x=int.from_bytes(d[1:5],'little');return (x&16383)+1,((x>>14)&16383)+1
        offset+=8+n+(n%2)
    raise ValueError('Missing WebP dimension chunk')

def set_attribute(tag,key,value):
    pattern=re.compile(r'\s'+re.escape(key)+r'\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+)',re.I)
    tag=pattern.sub('',tag)
    return tag[:-1]+f' {key}="{escape(str(value),quote=True)}">'

def bundle_url(original,name):
    return original.rsplit('/',1)[0]+'/'+name if '/' in original else name

def optimize_site(site):
    site=Path(site).resolve()
    if not (site/'assets').is_dir() or not (site/'build-manifest.json').is_file():
        raise ValueError('Expected a built GGC site directory, not source')
    manifest=site/'performance-manifest.json'
    if manifest.exists():raise ValueError('Already optimized; build into a fresh directory')
    original={str(p.relative_to(site)):digest(p.read_bytes()) for p in (site/'assets').iterdir() if p.is_file()}
    report={'version':VERSION,'pages':[],'bundles':{},'original_assets_sha256':original,
            'fonts':'same families/weights/display=swap; early HTML discovery and preconnect',
            'network_or_publication_performed':False,'inquiry_configuration_changed':False,
            'gzip_note':'gzip-9 byte estimates, not a claim about live Content-Encoding or user latency'}
    for page in sorted(site.rglob('*.html')):
        html=page.read_text(encoding='utf-8'); entries=[]
        for m in TAG.finditer(html):
            typ,a=attrs(m.group());url=a.get('href') if typ=='link' else a.get('src')
            p=local_file(site,page,url) if url else None
            entries.append((m,typ,a,p))
        styles=[e for e in entries if e[1]=='link' and e[2].get('rel')=='stylesheet' and e[3]]
        scripts=[e for e in entries if e[1]=='script' and e[3] and 'defer' in e[2] and 'async' not in e[2] and e[2].get('type','') in ['', 'text/javascript']]
        changes=[]; detail={'path':str(page.relative_to(site)),'html_bytes_before':len(html.encode()),'images':[]}
        for kind,items in [('css',styles),('js',scripts)]:
            if not items:continue
            forbidden={'media','disabled','title','integrity'} if kind=='css' else {'integrity','nomodule'}
            if any(forbidden&set(a) for _,_,a,_ in items):raise ValueError('Unexpected bundling semantics; inspect source first')
            pieces=[];fonts=[];before=[]
            for _,_,a,p in items:
                data=p.read_bytes();text=data.decode('utf-8');before.append(data)
                if kind=='css':
                    fonts.extend(IMPORT.findall(text));text=IMPORT.sub('',text)
                    if re.search(r'@(?:import|charset)\b',text):raise ValueError('Unrecognized CSS import/charset')
                    text=without_comments(text)
                elif any(x in text for x in ['document.currentScript','import.meta','document.write(']):
                    raise ValueError('A script requires per-file semantics; cannot bundle')
                pieces.append(text)
            body=('\n' if kind=='css' else '\n;\n').join(pieces)+'\n'
            data=body.encode();name=f'ggc-{kind}.{digest(data)[:16]}.{kind}';(site/'assets'/name).write_bytes(data)
            report['bundles'][name]={'type':kind,'raw_bytes':len(data),'gzip_estimate_bytes':gzlen(data),
                                    'inputs':[p.name for _,_,_,p in items],'sha256':digest(data)}
            first=items[0];url=bundle_url(first[2].get('href') or first[2].get('src'),name)
            if kind=='css':
                font_links=''
                if fonts:
                    font_links='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                    font_links+=''.join(f'<link rel="stylesheet" href="{escape(u,quote=True)}" data-ggc-fonts>' for u in dict.fromkeys(fonts))
                replacement=font_links+f'<link rel="stylesheet" href="{escape(url,quote=True)}" data-ggc-bundle="css">'
                detail['font_imports_before']=len(fonts);detail['font_imports_after']=0
            else:replacement=f'<script defer src="{escape(url,quote=True)}" data-ggc-bundle="js"></script>'
            changes.append((first[0].start(),first[0].end(),replacement))
            changes.extend((m.start(),m.end(),'') for m,_,_,_ in items[1:])
            detail[kind]={'requests_before':len(items),'requests_after':1,'raw_before':sum(map(len,before)),
                          'raw_after':len(data),'gzip_before':sum(map(gzlen,before)),'gzip_after':gzlen(data)}
        for m,typ,a,p in entries:
            if typ!='img' or not p or p.suffix!='.webp':continue
            w,h=webp_dimensions(p);tag=m.group()
            if 'width' not in a:tag=set_attribute(tag,'width',w)
            if 'height' not in a:tag=set_attribute(tag,'height',h)
            tag=set_attribute(tag,'decoding','async')
            # The approved cover uses max-height only. Width/height attributes must
            # not turn its auto-sized box into a fixed-width distorted box.
            if p.name=='book-cover.webp':
                tag=set_attribute(tag,'style','width:auto;height:auto;'+a.get('style',''))
            # These two explicit templates put the approved image in the hero.
            above=page.stem=='about' and p.name=='joyce-approved.webp' or page.stem=='book' and p.name=='book-cover.webp'
            if above:
                tag=set_attribute(tag,'loading','eager');tag=set_attribute(tag,'fetchpriority','high')
            elif page.stem=='index' and p.name=='joyce-approved.webp':tag=set_attribute(tag,'loading','lazy')
            changes.append((m.start(),m.end(),tag))
            detail['images'].append({'src':a['src'],'width':w,'height':h,'hero_priority':above})
        for start,end,repl in sorted(changes,reverse=True):html=html[:start]+repl+html[end:]
        # Empty layout headings have no information for assistive technology. Keep
        # the original element and margins, but remove its empty accessible heading.
        def quiet_heading(m):
            start=set_attribute('<'+m[1]+m[2]+'>','aria-hidden','true')
            return start+m[3]+'</'+m[1]+'>'
        html,count=re.subn(r'<(h[1-6])\b([^>]*)>(\s*)</\1>',quiet_heading,html,flags=re.I)
        detail['empty_headings_hidden']=count
        page.write_text(html,encoding='utf-8');detail['html_bytes_after']=len(html.encode());report['pages'].append(detail)
    for name,wanted in original.items():
        if digest((site/name).read_bytes())!=wanted:raise AssertionError('Original asset changed: '+name)
    report['original_assets_unchanged']=True
    report['locale_pages']=sum(p['path'].startswith(('zh/','en/')) for p in report['pages'])
    manifest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--site',type=Path,required=True)
    args=parser.parse_args();r=optimize_site(args.site)
    print(json.dumps({'pages':r['locale_pages'],'bundles':list(r['bundles']),'original_assets_unchanged':r['original_assets_unchanged']}))
