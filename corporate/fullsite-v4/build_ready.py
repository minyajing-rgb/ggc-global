#!/usr/bin/env python3
"""Generate an isolated PR11 P0-ready artifact; never deploy or change hosting.

The accepted 96-page builder and its 14 protected inputs remain unchanged.
Default is preview/noindex. Release requires an explicit canonical base URL.
"""
from pathlib import Path
import argparse, subprocess, sys, tempfile, shutil

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'readiness'))
from page_readiness import prepare_pages, validate_base_url


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--mode', choices=['preview', 'release'], default='preview')
    parser.add_argument('--base-url', required=True, help='Canonical HTTPS base chosen by the release owner; no DNS change is made.')
    args = parser.parse_args()
    canonical = validate_base_url(args.base_url)
    out = args.out.resolve()
    repo = HERE.parents[1]
    if out in [Path('/'), Path('/app'), Path.home(), repo] or out == HERE or out in HERE.parents or HERE in out.parents:
        raise SystemExit('Refusing to write in a source or system directory.')
    if out.exists() and any(out.iterdir()):
        raise SystemExit('Output must be new or empty; use a separate candidate directory.')
    with tempfile.TemporaryDirectory(prefix='ggc-pr11-build-') as temp:
        temp = Path(temp)
        candidate, stage = temp / 'site', temp / 'source'
        subprocess.run([sys.executable, str(HERE / 'prepare_site.py'), '--out', str(candidate), '--stage', str(stage)], check=True)
        prepare_pages(candidate, HERE / 'readiness', args.mode, canonical)
        shutil.copytree(candidate, out, dirs_exist_ok=True)
    print(f'P0 artifact: {out}; mode={args.mode}; canonical={canonical}; not deployed')


if __name__ == '__main__':
    main()
