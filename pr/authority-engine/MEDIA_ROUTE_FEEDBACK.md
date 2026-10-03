# GGC — Media Route and Format Feedback

Updated: 2026-10-03

This is a sanitized operational decision log. The original two Gmail threads were read and reconciled on 2026-10-03. Raw correspondence, headers, message / thread IDs and non-public contact details remain outside this public repository. Feedback IDs below are local decision keys, not Gmail IDs.

## Reconciled decisions

| Feedback ID | Outlet / route | Feedback date | Classification | Decision |
|---|---|---|---|---|
| `MG_FORMAT_2026_10_01` | MobileGamer.biz / Neil Long, Founder + Editor | 2026-10-01 | Human format rejection | Close the AI creative-volume vs retention operator-interview proposal. Suppress generic operator-interview and uncommissioned operator thought-leadership pitches for this outlet, including materially similar H2/H3/H6 proposals. No follow-up or alternate-contact bypass. |
| `TIA_ROUTING_2026_10_01` | Tech in Asia / editorial desk | 2026-10-01 | Automated routing only | Keep independent editorial as a normal route, with human interest unconfirmed. Separate the paid Press Release and BD / marketing options; neither is an editorial progression. |

Scope: the MobileGamer decision concerns the submitted format and materially similar proposals. It is not evidence that the outlet never interviews anyone, a permanent all-topic opt-out, or a rejection of Joyce's expertise. A different future news / data tip requires a fresh concrete hook, evidence and format review; it cannot be a repackaged interview request.

## Route map

| Outlet / lane | Official source / entry | Qualification / cost state | Operating action |
|---|---|---|---|
| MobileGamer.biz / potential different editorial tip | [Site and coverage](https://mobilegamer.biz/) | News and data coverage observed 2026-10-03; no new tip or interview acceptance verified. The existing graph's advertising-page source is not evidence of interview fit. | Keep the generic interview / thought-leadership suppression. Research only for a materially different concrete story; do not send now. |
| Tech in Asia / independent editorial | [Coverage guideline](https://help.techinasia.com/support/solutions/articles/17000012882-how-do-i-get-covered-by-tech-in-asia-) | Official guideline retrieved 2026-10-03; page states last modified 2019-11-14. The 2026-10-01 routing response independently confirms that the original editorial desk is the right place for coverage. | Prepare an Asia-relevant reported story / trend memo with evidence and why now. Current pitch remains awaiting human editorial judgment. |
| Tech in Asia / paid Press Release | [PR form link supplied by the automated response](https://techin.asia/pr-editors) | US$500 one-time price quoted in the 2026-10-01 auto-response. The short URL could not be retrieved independently on 2026-10-03; current form / price / terms not rechecked. | `PAID_PR`; exclude from earned-media shortlist. No purchase, payment or paid-form submission authorized. |
| Tech in Asia / BD / marketing partnership | [Commercial link supplied by the automated response](https://techin.asia/advertise-editors) | Commercial partnership / marketing lane; price unknown. The short URL could not be retrieved independently on 2026-10-03. | `COMMERCIAL_PARTNERSHIP`; exclude from earned editorial. No redirection of the story pitch or partnership outreach authorized by this update. |

The Tech in Asia editorial guideline separates independent coverage from branded content and describes news, profiles, trend analysis and company-building advice formats. Route availability does not mean the current story is accepted or that an editor has read it.

## Measurement correction

For these two reconciled conversations: **1 human reply (negative format feedback), 1 automated routing response, 0 positive editorial replies**. Do not infer the full batch's conversion rate from this subset. Commercial route records are not additional human contacts or editorial leads.

## Additional batch reconciliation — 2026-10-03

The remaining seven original PR / speaking threads and Data Summit's separate form receipt were read during the follow-up status check. This supersedes the earlier unreconciled state for those specific records.

| Feedback ID | Outlet / opportunity | Evidence state | Action |
|---|---|---|---|
| `VB_BOUNCE_2026_10_01` | VentureBeat / original named primary recipient | Delivery report on 1 Oct confirms a 550 / 5.1.1 address-not-found hard bounce for the primary address. The CC news-desk recipient's delivery is not established by that report. | Stop reuse of the failed primary address; reverify an official current route before any future touch. Preserve CC delivery / human interest as unconfirmed; no automatic resend. |
| `BATCH_NO_HUMAN_2026_10_03` | PocketGamer.biz, TechTarget, e27, GamesBeat; PG Connects San Francisco speaking proposal | Each original thread has the sent first touch only at this check; no human response or scheduled conversation verified. | Maintain unconfirmed response state; no connection, follow or interview claim. |
| `DATA_SUMMIT_INTAKE_2026_10_02` | Data Summit 2027 | A human programme response directed submission through the official form; a separate organizer form receipt on 2 Oct confirms receipt for review. | Submitted / awaiting selection; no duplicate proposal. The process reply is not substantive programme interest, and the receipt is not acceptance. |

Across the original **7 media conversations**: 1 format rejection, 1 automated routing response, 1 partial delivery failure with CC delivery unconfirmed, and 4 threads with no human reply verified. **0 positive editorial replies and 0 scheduled media interviews verified.** Across the **2 speaking conversations**: Data Summit has a received form submission awaiting review; PG Connects San Francisco has no human response verified. Personal-channel adds / follows were not confirmed by this email audit.

## Graph field contract

The original 11 CSV columns are preserved. Appended fields support route / format selection without rewriting contact verification history:

| Field | Meaning |
|---|---|
| `record_kind` | `TARGET_SEED` for the original 128 records; `ROUTE_ONLY` for the two separately recorded commercial lanes. Neither alone implies outreach readiness. |
| `route_type` | Candidate editorial, podcast, research / vendor content, programming, ecosystem or mixed lane; confirmed Tech in Asia editorial, paid PR and commercial lanes are separate. Candidate labels are inferred from the original type / role, not verified intake policies. |
| `selected_format` / `supported_formats` | The sent / proposed deliverable versus formats evidenced by a guideline or coverage. Empty means not established; do not default to an interview. |
| `blocked_formats` | Semicolon-separated outlet-level suppression. Apply across contacts and hooks, including materially similar renamed pitches. |
| `format_fit` | `UNVERIFIED`, `MISMATCH`, `GUIDELINE_CONFIRMED_STORY_PENDING`, or `NON_EDITORIAL_ROUTE`. Only an actual matched format with dated evidence can pass future qualification; official guidelines still leave story selection to editors. |
| `format_evidence_url` / `format_checked_at` | Public supporting URL and review date. Reply-based suppression uses the linked sanitized decision log. |
| `reply_class` | Reconciled response classification; `NOT_RECONCILED` means no inference was made about other threads. |
| `editorial_interest` | `REJECTED_FORMAT`, `NOT_CONFIRMED`, `NOT_APPLICABLE` or `NOT_RECONCILED`; only a later substantive human editorial response can establish interest. |
| `follow_up_policy` | Fit review required, stop rejected format, await human response without an auto-trigger, or commercial-only hold. Original same-outlet / sent states remain binding. |
| `fee_usd` / `payment_authorization` | Dated quoted price where known, and authorization state. Empty price means unknown / not established, not free. |
| `next_action` | Outlet-specific preparation or hold instruction; no send permission implied. |
| `feedback_date` / `feedback_ref` | Feedback event date and local key in this document. |

## Future shortlist rule

1. Select channel and exact format before drafting, using official guidance or comparable recent coverage.
2. Apply outlet-format suppression and original contact-state holds before priority ranking.
3. Exclude paid PR and commercial partnerships from earned-editorial queues and KPIs.
4. Leave unknown routes / formats in research; organization / contact verification is insufficient.
5. Tailor the story, evidence and requested deliverable to the chosen outlet. Reuse evidence where useful, not the same generic interview ask.
6. Reconcile real human replies separately from routing messages before selecting follow-ups.

No external messages, payments or new outreach automation were performed as part of this reconciliation.
