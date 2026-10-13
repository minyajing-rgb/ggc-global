# AI workspaces in the GGC product directory

The bilingual product directory adds two public product entries:

- [Seven Agent Office](https://ai.ggcgames.com/): browser-local workflow simulation, with manual controls and local saves.
- [Cat Workspace](https://agency.ggcgames.com/): sanitized GPT / Codex work status. Six occupational cat costumes, sanitized history playback and manual local simulation. Two Codex roles use local turn metadata; four GPT roles use desktop cache. Visual movement is not completion or delivery evidence.

Both entries use branding cropped from their actual product header and real UI captures. `ai-workspaces-assets.json` records the public source URL, capture hash and exact crop for every derived image. No new product logo or promotional illustration is generated.

`ai_workspaces.py` runs after the accepted V4 builder. It adds the two software entries and an accessible product search field using the existing filter/search behavior. The accepted 14 source and asset hashes remain unchanged. The independent Ops Cat mowing showcase from `a7ab052` is retained, with its original assets and game entry.

Build with the bundled Python runtime on macOS; the system Apple Python 3.9 can reject the existing UTF-8 builder on direct execution, while the bundled runtime builds the unchanged protected source successfully.

```sh
/Users/joyce/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 corporate/fullsite-v4/build_ready.py --out /tmp/ggc-ai-products-candidate --mode release --base-url https://ggcgames.com/ --google-form
```

Publishing remains a separate release operation through the existing corporate publication workflow. This source change does not change product access, credentials, forms or deployment settings.
