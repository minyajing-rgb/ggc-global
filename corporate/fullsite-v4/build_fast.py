#!/usr/bin/env python3
"""Build the current P0-ready site, then apply the reviewed performance layer.
Same source and gated inquiry mode as build_ready.py. Does NOT deploy anything.
"""
from pathlib import Path
import argparse, shutil, subprocess, sys, tempfile
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'performance'))
from optimize_site import optimize_site

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--mode',choices=['preview','release'],default='preview')
    p.add_argument('--base-url',required=True)
    p.add_argument('--inquiry-endpoint',help='Explicit existing reviewed endpoint only; never enabled by optimization')
    a=p.parse_args();out=a.out.resolve();repo=HERE.parents[1]
    if out in [Path('/'),Path('/app'),Path.home(),repo] or out==HERE or out in HERE.parents or HERE in out.parents:
        raise SystemExit('Refusing unsafe output directory')
    if out.exists() and (not out.is_dir() or any(out.iterdir())):raise SystemExit('Output must be new or empty')
    with tempfile.TemporaryDirectory(prefix='ggc-fast-') as tmp:
        candidate=Path(tmp)/'site'
        command=[sys.executable,str(HERE/'build_ready.py'),'--out',str(candidate),'--mode',a.mode,'--base-url',a.base_url]
        if a.inquiry_endpoint:command+=['--inquiry-endpoint',a.inquiry_endpoint]
        subprocess.run(command,check=True)
        result=optimize_site(candidate)
        shutil.copytree(candidate,out,dirs_exist_ok=True)
    print(f'Performance candidate: {out}; {result["locale_pages"]} localized pages; not deployed')
if __name__=='__main__':main()
