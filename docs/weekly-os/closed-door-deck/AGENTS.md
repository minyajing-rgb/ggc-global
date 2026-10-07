# Instructions for this closed-door deck

Scope: this directory and all its generated batches, images and PDFs. This is Joyce/GGC's 29-page closed-door executive showcase, not the older Weekly OS reporting template.

## Before editing or generating

Read `README.md`, `MASTER_29P.md`, `OUTLINE_AND_COVERAGE.md`, `STYLE_AND_QA.md`, and `manifest.json`. Run `python verify.py`. Record the actual Git commit used for the batch. Do not work from conversation memory or copy text from attractive reference images.

The master contains the complete user-selected v8 on-screen text, with a real book page at S04. There are exactly 29 pages. Do not change wording, titles, data, order, book, product names or contact details while redesigning. If the user explicitly changes copy, make a new version and record the difference; never silently regenerate old checksums to hide changes.

## Content and positioning

Keep the executive-level focus: Joyce's experience and results; GGC's business and professional assets; ongoing products; long-term creative/connection vision; selected paid cooperation. Show problems, role, outputs and results, not step-by-step techniques. Do not turn this into a Game OS product pitch or an AI tutorial. Do not insert agenda filler or split already-merged subjects again.

Preserve distinctions between historic results, projections, prototypes, interface mockups, reference prices and dated product snapshots. No new business facts, client identities, unsupported logos, performance numbers or private narratives may be introduced.

## Visual rules

Read STYLE_AND_QA instead of the older parent Weekly OS template. White-dominant poster-style pages, bold normal-proportion type, small iridescent accents and very pale panels. No solid hot-pink card backgrounds; no gradient rectangles covering text; no clipped headings. One independent 16:9 PNG per page; compose the PDF from verified PNGs.

Portrait: S01 only, directly composite the real AY4A7260(5).jpg photo with its original proportions. Do not redraw or reshape the face. Book: S04, use the real supplied book-cover crop, not a generated book. Asset hashes and reference roles are in STYLE_AND_QA. Their registration does not imply image binaries have been uploaded in this task.

## Every batch

Prepare exact input with `python verify.py --prepare 01-10 --commit <actual-40-character-commit>` (then 11-20 and 21-29). Generate from these page sections. Open each result and compare title/body, numbers/units/qualifiers, style, crop/clipping, original assets and privacy. Record specific observations in the batch's qa.json and the actual image hash. Unknown or unchecked is not PASS. Failed pages must be redone.

`verify.py --review ...` checks files, hashes, dimensions and recorded visual checks; it does not read image text or establish business truth. Do not claim user approval unless the user actually approved the images. Before PDF assembly, check all 29 pages at one baseline, one size, in order, with no missing or duplicate pages.

## Repository and disclosure

This repository is public. Only upload the desensitized approved copy and allowed public assets. Keep private family material, client confidential records, raw user data, credentials and internal technical details out. Do not modify the website, PR status files, unrelated workflows or the older Weekly OS template while working on this deck.
