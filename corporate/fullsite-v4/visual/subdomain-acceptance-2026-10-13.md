# GGC public subdomain gate — 2026-10-13

This is a public HTTP/content pass, not a functional or account-security certification. A 200 response alone does not qualify a site for the corporate navigation.

| Host | Public observation | Corporate-site decision |
| --- | --- | --- |
| `ggcgames.com`, `www.ggcgames.com` | HTTPS 200; `www` resolves to root | Main corporate site; keep |
| `biz.ggcgames.com` | HTTPS 200; complete Joyce/GGC services site and rate-card path | Keep the existing contextual rate-card link |
| `mow.ggcgames.com` | HTTPS 200; playable Ops Cat yard UI | Hold from navigation pending gameplay/product acceptance |
| `opsgo.ggcgames.com` | HTTPS 200; root exposes a project page index and unfinished content | Remove direct outbound links; point OpsGo references to reviewed GGC product catalog |
| `ai.ggcgames.com` | HTTPS 200; explicitly labeled v0.1 simulation, not live agents | Hold from navigation |
| `agency.ggcgames.com` | HTTPS 200; public desensitized workspace view | Hold pending content and privacy review |
| `job.ggcgames.com` | HTTPS 200; sparse “简适AI” shell | Hold |
| `kol.ggcgames.com`, `hpdf.ggcgames.com`, `rader.ggcgames.com` | HTTPS 200; project/page-directory or thin landing content | Hold pending page-by-page product acceptance |
| `infra.ggcgames.com` | HTTPS 200; Slidev deck shell | Internal/reference only |
| `pr.ggcgames.com`, `ops.ggcgames.com`, `iet.ggcgames.com` | No usable HTTPS response in this pass | Hold; diagnose DNS/hosting separately |
| `checkout.ggcgames.com` | HTTPS 204 | Service endpoint; never present as a public page |

Next gate for each held public product: open it in a browser, verify the primary action and supporting pages, check mobile layout and privacy/identity text, then add a link only when that individual product passes.
