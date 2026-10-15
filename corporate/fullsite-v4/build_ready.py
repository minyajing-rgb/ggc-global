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
from product_links import align_product_links
from book_release import add_book_release


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--mode', choices=['preview', 'release'], default='preview')
    parser.add_argument('--base-url', required=True, help='Canonical HTTPS base chosen by the release owner; no DNS change is made.')
    parser.add_argument('--inquiry-endpoint', help='Optional reviewed FormSubmit AJAX endpoint for live business inquiries in release mode only.')
    parser.add_argument('--google-form', action='store_true', help='Use the reviewed Google Forms enquiry link in release mode.')
    args = parser.parse_args()
    canonical = validate_base_url(args.base_url)
    if args.inquiry_endpoint and (args.mode != 'release' or args.inquiry_endpoint != 'https://formsubmit.co/ajax/minyajing@gmail.com'):
        raise SystemExit('Only the reviewed GGC FormSubmit endpoint may be enabled in release mode.')
    if args.google_form and (args.mode != 'release' or args.inquiry_endpoint):
        raise SystemExit('The Google form requires release mode and cannot be combined with FormSubmit.')
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
        prepare_pages(candidate, HERE / 'readiness', args.mode, canonical, args.inquiry_endpoint, args.google_form)
        align_product_links(candidate)
        add_book_release(candidate)
        shutil.copytree(candidate, out, dirs_exist_ok=True)
    print(f'P0 artifact: {out}; mode={args.mode}; canonical={canonical}; not deployed')


if __name__ == '__main__':
    main()
