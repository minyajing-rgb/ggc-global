"""Apply the additive public evidence update to the existing approved HTML."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / "docs/site-evidence"))
from public_content import apply_biz, CSS
pages=[ROOT/"index.html",ROOT/"joyce/index.html"]
if all("data-proof-version=" not in p.read_text() for p in pages):
    apply_biz(ROOT)
elif not all("data-proof-version=" in p.read_text() for p in pages):
    raise RuntimeError("Mixed source states; review before updating")
(ROOT/"joyce/assets/operating-proof.css").write_text(CSS)
print("Operating evidence present at both entry points")
