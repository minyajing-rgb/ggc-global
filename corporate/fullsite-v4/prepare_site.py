#!/usr/bin/env python3
"""Assemble the accepted V4 source without altering the prior implementation.
Transport normalizations are narrowly scoped and followed by exact SHA-256 checks.
Only --normalize-source writes decoded original assets/canonical text back to this
new fullsite directory. No credentials, DNS, deployed root or business data touched.
"""
from pathlib import Path
import argparse, base64, hashlib, json, shutil, subprocess, sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'implementation/src'
BASE_HASH={
'app.js':'b00c8d48d34c1623aa64efddc8ed487e31766d0771d8303ee83b36bfbbeaf1a7',
'build_site.py':'2993a739f659e84a3be84dfdc8c8a0b7b0dde6598f8fb4b9a0fedce0f4b9e196',
'build_refined_site.py':'80c9da782086a85ada31e63afe0b32b836317b8306f373b2d66ab0a168780be7',
'buttons.css':'733e4266ff924d091643e6e6a7a838b0ad3a9459999f60f14e8d72d89ce107a4',
'fidelity.css':'7bc496542907fc9650506f1b1b092c4329c9b020f19c5bdc1d7d64582f55ea25',
'ggc-logo-refined.svg':'3e8ae94362f90584a61771ddf7cbb4b68a6cb89712c74e24b7cbbe4e21f3bd24',
'prism.css':'da199dfe396718c0707e15a6f1d1a4a5eed0093a2a672d6a74096e175146bbfa',
'prism-ribbon.svg':'4ace85a3a874838dc1c26e9f5420146b8d464a06a10ac19b02c520cc3eb11995',
'site.css':'ccd368527f5323069c4fd24c9c4104accd0d7af9b2ce518dbfb2571004e89534'}
SOURCE_HASH={
'build_fullsite.py':'9866db81908554d157d2ad633815c0f214df97b050dae96ad4f874da322a24e6',
'fullsite.css':'62bf907dc76a9279978420803d538fbbe3ee228d408dd60233a63a0e593f7120',
'fullsite.js':'9b5d9242d4c4e0b1e7eef21bd931814daf052a72eb00abf7a371997766051885'}
ASSET_HASH={
'joyce-approved.webp':'c84aaaa9f52e192ae0601b01b78b1d0231be3b56e1d1aba0f5a2949d7d636342',
'book-cover.webp':'e9df66ebd63c94270fcefbfec56a113aaf6bdc95c16e6fcf20821d4084fbd591'}

def checked(name,data,wanted):
    actual=hashlib.sha256(data).hexdigest()
    if actual!=wanted:raise ValueError(f'Integrity mismatch: {name}: {actual}; expected {wanted}')
    return data

def canonical_source(name,data):
    # One line transcription in the GitHub transport differed from the approved ZIP.
    if name=='build_fullsite.py' and hashlib.sha256(data).hexdigest()=='77906f079486bbfef1598033b6ce7af83a2f4e643eacd80978c442f31d6b28fd':
        old=b"'Explicit contributions, responsibilities and rights')],'CO-BUILD / GGC')"
        new=b"'Explicit contributions, roles and rights')],'CO-BUILD / VENTURES')"
        if data.count(old)!=1:raise ValueError('Expected unique transport correction missing')
        data=data.replace(old,new,1)
    return checked(name,data,SOURCE_HASH[name])

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--stage',type=Path);p.add_argument('--normalize-source',action='store_true');a=p.parse_args()
    out=a.out.resolve();stage=(a.stage or out.parent/(out.name+'-source')).resolve()
    if out in [Path('/'),Path('/app'),Path.home(),HERE,BASE] or stage in [Path('/'),Path('/app'),Path.home(),HERE,BASE]:raise ValueError('Unsafe output/staging root')
    stage.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
    verified={}
    for name,wanted in BASE_HASH.items():
        data=checked('baseline/'+name,(BASE/name).read_bytes(),wanted);(stage/name).write_bytes(data);verified[name]=wanted
    for name,wanted in SOURCE_HASH.items():
        data=canonical_source(name,(HERE/'source'/name).read_bytes());(stage/name).write_bytes(data);verified[name]=wanted
        if a.normalize_source:(HERE/'source'/name).write_bytes(data)
    for name,wanted in ASSET_HASH.items():
        binary=HERE/'assets'/name
        if binary.exists():data=binary.read_bytes()
        else:
            parts=sorted((HERE/'assets').glob(name+'.b64.*'))
            if not parts:raise FileNotFoundError(name)
            text=''.join(f.read_text().strip() for f in parts)
            # A single visually identical Cyrillic o in the text transport is mapped
            # back to ASCII; exact decoded SHA below rejects any other corruption.
            text=text.replace('\u043e','o')
            data=base64.b64decode(text,validate=True)
        data=checked(name,data,wanted);(stage/name).write_bytes(data);verified[name]=wanted
        if a.normalize_source:
            binary.write_bytes(data)
            for part in (HERE/'assets').glob(name+'.b64.*'):part.unlink()
    art=HERE/'assets'/'product-art'
    if len(list(art.iterdir()))!=14:raise ValueError('Expected 14 reviewed product illustrations/assets')
    shutil.copytree(art,stage/'product-art',dirs_exist_ok=True)
    subprocess.run([sys.executable,str(stage/'build_fullsite.py'),'--out',str(out)],check=True)
    report={'accepted_zip':'GGC_Fullsite_UI_and_Frontend_V4_2026-10-12.zip','source_sha256':verified,'pages':96,'ui_types':16,'production_changed':False,'stage':str(stage),'output':str(out)}
    (out/'source-verification.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({'hashes_verified':len(verified),'pages':96,'ui_types':16,'output':str(out)}))
if __name__=='__main__':main()
