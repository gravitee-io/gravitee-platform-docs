# Gamma top-level navigation redirect plan (DOC-1831)

This plan proposes the redirect map and rollout sequence for promoting the six Gamma modules to top-level sections of `documentation.gravitee.io`, replacing the single `gravitee-gamma` section. It implements DOC-1831 inside the DOC-1826 navigation migration epic. Sibling tickets: DOC-1848 (six-module navigation), DOC-1849 (enable in production), DOC-1832 (test and fix), and DOC-1850 (404 tracking).

This folder sits outside every space-bound `docs/` directory, so GitBook never publishes it, and merging this plan changes nothing on the live site. Every mapping stays a proposal until the open decisions at the end are signed off.

## End state

The migration turns the six top-level navigation groups of the Gamma space into six site sections, each with its own URL slug and its own top-nav tab.

Live top-level sections on 2026-08-04, from the root sitemap:

| Section | Live URLs (default version) | Archive URLs |
| --- | --- | --- |
| Home (no slug) | 1 | none |
| `/apim` | 553 | about 3,572 across `4.0` to `4.11` |
| `/am` | 173 | about 1,668 across `4.0` to `4.11` |
| `/gravitee-kubernetes-operator-gko` | 60 | about 345 across `4.3` to `4.11` |
| `/gravitee-cloud` | 41 | none |
| `/gravitee-gamma` | 152 | none |
| `/edge-stack` | listed in the root sitemap, but its page sitemap returned zero URLs on 2026-08-04 | none |

Target top navigation: Home plus the six module sections.

| Module | Slug | Live URLs today under `/gravitee-gamma` |
| --- | --- | --- |
| Platform Management | `/platform-management` | 31 |
| API Management | `/api-management` | 24 |
| Event Stream Management | `/event-stream-management` | 13 |
| Agent Management | `/agent-management` | 40 |
| Authorization Management | `/authorization-management` | 36 |
| Edge Management | `/edge-management` | 7 |

All six slugs returned 404 on 2026-08-04, so they're unclaimed and collide with no live section. Note that `/api-management` and the existing `/apim` are different routes, so both can serve during the transition. The remaining URL of the 152 is the space root `/gravitee-gamma` itself.

Example transform: `https://documentation.gravitee.io/gravitee-gamma/platform-management/overview` becomes `https://documentation.gravitee.io/platform-management/overview`.

Versioning follows the `/apim` convention: the bare section path serves the default version, and archive versions serve under a version segment such as `/apim/4.11/`. Verified for `/apim` on 2026-07-22: `/apim/4.12` returns 307 to bare `/apim`, and `/apim/4.11` serves the archive variant.

### Repo shape

Each module folder under `docs/gamma/<version>/` becomes its own GitBook space root (DOC-1848 scope, separate PR). Proposed skeleton per module folder, matching the existing space configuration in `docs/gamma/4.12/.gitbook.yaml`:

```yaml
root: ./

structure:
  readme: README.md
  summary: SUMMARY.md
```

Each module also needs its own `SUMMARY.md` (its slice of the current `docs/gamma/<version>/SUMMARY.md`, with paths rebased) and a `README.md` landing page. The six modules already exist as the top-level groups of `docs/gamma/4.12/SUMMARY.md`, so the slicing is mechanical.

## Redirect mechanisms and constraints

Five facts decide which mechanism serves which redirect.

- `redirects:` entries in a space `.gitbook.yaml` are space scoped, and each target must be a real `.md` file inside that space. They can't redirect across sections, and they stop working when their section is removed. Verified 2026-06-10 during the platform-overview removal.
- The `redirects:` block in the repo-root `.gitbook.yaml` never fires. Verified 2026-07-22: `/ae` and `/alert-engine` returned 404 despite entries there. That file serves only as a registry of historical mappings.
- Site redirects (site settings, Redirects) are URL-route rules. They work across sections and versions, and per the GitBook documentation they support trailing wildcards (`/docs/*`) with an option to append the matched text to the destination, plus CSV import of up to 500 rows per import. A management API also exists (`POST /v1/orgs/{organizationId}/sites/{siteId}/redirects`). Wildcard behavior and the API are external product features that haven't been tested here: verify both with a test rule at execution time. References: [Site redirects](https://gitbook.com/docs/docs-site/site-redirects) and the [site redirects API](https://gitbook.com/docs/developers/gitbook-api/api-reference/docs-sites/site-redirects).
- GitBook auto-redirects survive page moves and renames made in the editor. Verified 2026-08-03: 8 legacy Gamma URLs returned 307 with no explicit rule.
- GitBook auto-redirects don't survive section removal, slug renames, or page deletions. Verified 2026-08-03: 14 legacy Gamma URLs returned 404 until PR #2124 added explicit rules. Don't rely on auto-redirects for this migration.

One more behavior matters for target selection: published URLs follow the navigation tree, not repo file paths. Verified 2026-08-03: `agent-management/build/edit-mcp-studio-composition.md` serves under `agent-management/build/create-an-mcp-studio/`.

## Redirect map

The full map ships in [`url-map.yaml`](url-map.yaml) in this folder, split into three tiers.

### Tier 1: re-home the 152 live Gamma URLs

The rule is mechanical: strip the `/gravitee-gamma` prefix. `/gravitee-gamma/<module>/<path>` becomes `/<module>/<path>` for all 151 module URLs, and the space root `/gravitee-gamma` goes to `/` (proposed, open decision 5). All 152 sources returned 200 on 2026-08-04.

Two implementation options:

1. Wildcard-first (preferred if verification passes): one site redirect per module, `/gravitee-gamma/<module>/*` to `/<module>/*` with matched-text replacement enabled, plus one exact rule for the root. Seven rules total. The 152-row list in `url-map.yaml` then serves as the verification checklist.
2. Exact-path fallback: import all 152 rows (one CSV import, under the 500-row limit) if wildcard behavior doesn't verify.

These must be site redirects either way: after the cutover no space owns the `/gravitee-gamma/*` routes, so space YAML can't serve them.

### Tier 2: re-base the 14 legacy redirects from PR #2124

`docs/gamma/4.12/.gitbook.yaml` and `docs/gamma/4.13/.gitbook.yaml` (lines 7 to 21 in both) carry 14 `redirects:` entries covering pre-restructure URLs. Those entries die with the `gravitee-gamma` section, so each source needs an exact-path site redirect. Wildcards can't serve these: the sources live under renamed paths (`event-management`, `edge-daemon`, `explorer`) whose targets don't share their sub-path.

Each row below was captured live on 2026-08-04: every source returned 307 to the listed current target.

| Source (unchanged after cutover) | Current live target | Target after cutover |
| --- | --- | --- |
| `/gravitee-gamma/agent-management/edge-daemon` | `/gravitee-gamma/edge-management/get-started` | `/edge-management/get-started` |
| `/gravitee-gamma/agent-management/edge-daemon/connect-claude-code-to-daemon` | `/gravitee-gamma/edge-management/connect` | `/edge-management/connect` |
| `/gravitee-gamma/agent-management/import/create-event-tools` | `/gravitee-gamma/agent-management/import` | `/agent-management/import` |
| `/gravitee-gamma/authorization-management/build` | `/gravitee-gamma/authorization-management/get-started` | `/authorization-management/get-started` |
| `/gravitee-gamma/authorization-management/build/create-authorization-policies` | `/gravitee-gamma/authorization-management/configure/create-update-delete-policies` | `/authorization-management/configure/create-update-delete-policies` |
| `/gravitee-gamma/event-management/build/create-a-kafka-service` | `/gravitee-gamma/event-stream-management/build/create-a-kafka-service-with-a-registered-cluster` | `/event-stream-management/build/create-a-kafka-service-with-a-registered-cluster` |
| `/gravitee-gamma/event-management/explorer` | `/gravitee-gamma/event-stream-management/get-started` | `/event-stream-management/get-started` |
| `/gravitee-gamma/event-management/explorer/create-kafka-topics` | `/gravitee-gamma/event-stream-management/get-started` | `/event-stream-management/get-started` |
| `/gravitee-gamma/event-management/explorer/inspect-kafka-messages` | `/gravitee-gamma/event-stream-management/get-started` | `/event-stream-management/get-started` |
| `/gravitee-gamma/event-management/explorer/manage-connections` | `/gravitee-gamma/event-stream-management/get-started` | `/event-stream-management/get-started` |
| `/gravitee-gamma/event-management/get-started` | `/gravitee-gamma/event-stream-management/get-started` | `/event-stream-management/get-started` |
| `/gravitee-gamma/event-management/get-started/create-your-first-kafka-topic` | `/gravitee-gamma/event-stream-management/get-started` | `/event-stream-management/get-started` |
| `/gravitee-gamma/event-management/get-started/event-management-overview` | `/gravitee-gamma/event-stream-management/get-started/event-stream-management-overview` | `/event-stream-management/get-started/event-stream-management-overview` |
| `/gravitee-gamma/platform-management/manage-the-platform` | `/gravitee-gamma/platform-management/overview` | `/platform-management/overview` |

### Tier 3: legacy product sections

Tier 3 depends on the open decisions and ships no rules that are ready to apply yet. The recommended primary path keeps the legacy sections published while their content consolidates into the modules product by product, which keeps the day-one map at tiers 1 and 2 (21 rules on the wildcard path, 166 on the fallback path). If a legacy section is removed instead, every URL under it needs redirect coverage before removal.

Destination candidates:

| Legacy section | Candidate destination | Status |
| --- | --- | --- |
| `/apim` | `/api-management`, with the Kafka Gateway subtree a candidate for `/event-stream-management` and the agent mesh and MCP subtree a candidate for `/agent-management` | Candidate |
| `/gravitee-cloud` | `/platform-management` (control plane, organizations, and environments) | Candidate |
| `/gravitee-kubernetes-operator-gko` | `/api-management` (deploy tooling for API resources), alternative `/platform-management` | Candidate |
| `/am` | Open product decision, see below | Pending decision |
| `/edge-stack` | No default match, see below | Pending decision |

Access Management detail: the Authorization Management module covers policy authorization, while Access Management covers identity concerns such as identity providers, MFA, and OAuth and OpenID Connect flows. A name-level match isn't a concern-level match. Candidate homes: `/authorization-management` with an identity area, `/platform-management` as platform identity infrastructure, or Access Management stays a published section until a Gamma identity home exists.

Edge Stack detail: the Edge Management module documents the edge daemon surface. Its 4.12 content is `connect/`, `get-started/`, `observe/`, and daemon connection pages (verified from the `docs/gamma/4.12/edge-management/` folder contents on 2026-08-04). Edge Stack is an ingress product, so `/edge-stack/*` doesn't map to `/edge-management/*` by concern, and its disposition needs its own decision.

Archive versions: about 5,585 archive URLs exist across `/apim`, `/am`, and `/gravitee-kubernetes-operator-gko`. They enter scope only under a remove-at-flip decision. Precedent exists for both exact deep targets and landing collapse in the legacy release-notes and Alert Engine redirect work (PR #1974 and PR #2019).

## Rollout runbook

The sequence aligns with DOC-1849 and keeps every step reversible until the section removal.

1. Land the DOC-1848 repo prep: per-module `.gitbook.yaml`, `SUMMARY.md`, and `README.md` under `docs/gamma/<version>/<module>/`.
2. Create the six GitBook spaces and bind git sync to this repo, branch `main`, project directory `docs/gamma/<version>/<module>`. The project directory must be the subpath, and the initial sync direction must be GitHub to GitBook: the wrong direction overwrites the repo (verified during the 2026-06-29 Gamma flip).
3. Add the six sections to the site with the slugs above. Confirm in the UI whether new sections can stay unlisted until the flip.
4. Verify wildcard redirect behavior with one test rule, then apply tier 1 and tier 2 from `url-map.yaml` through the Redirects settings, CSV import, or the site redirects API.
5. Review existing site redirects in the UI for any rule whose destination points into `/gravitee-gamma/`, and re-base those destinations.
6. Remove the `gravitee-gamma` section and its top-nav tab from the site.
7. Re-run the DOC-1832 sweep against the new URL space: the 152-URL list, the 14 tier-2 sources, and the 75-URL historical set, expecting 307 responses that land on 200 pages. After the PR #2124 merge, GitBook applied redirects within about a minute, with mixed responses for about 5 minutes of CDN propagation.
8. Track stragglers through DOC-1850 and the monthly 4XX report.

## Risks

- Bi-directional git sync: GitBook editor commits write back to `main` and can conflict with open PRs during the transition. Merge fast, or edit through PRs only.
- SEO: every redirect observed above returns 307, and the GitBook documentation describes automatic redirects as HTTP 307. Whether a 301 option exists isn't stated there. Flag to the SEO owner before cutover.
- Hidden pages: 7 Gamma repo pages carried `hidden: true` on 2026-08-03 and stay excluded from redirect targets. Re-check at execution.
- Slug collisions are zero today and stay zero only while nothing else claims the six slugs. Re-run the six-slug 404 check right before the flip.
- Version overrides: this plan adds no files under versioned docs folders, so no `.version-overrides` entries apply here. The DOC-1848 restructure PR needs them for any file added under a newer version folder.

## Open decisions

1. Legacy sections at cutover: keep them published while content consolidates (recommended), or remove them at the flip with full per-URL coverage first.
2. Access Management destination (tier 3).
3. Kubernetes Operator destination: `/api-management` or `/platform-management`.
4. Edge Stack disposition.
5. Target for the `/gravitee-gamma` space root (`/` proposed).
6. Reconciliation: no already-agreed module-to-path mapping was found in Jira, this repo, or the docs-workflows repo on 2026-08-03. If one exists elsewhere, reconcile it with `url-map.yaml` before applying anything.
7. Redirect status code for SEO (307 observed).

## Verification table

| # | Claim | Verdict | Source |
| --- | --- | --- | --- |
| 1 | Live sections and per-section URL counts | Verified 2026-08-04 | Root sitemap and every per-section `sitemap-pages.xml` on `documentation.gravitee.io` |
| 2 | Each of the six target slugs returns 404 | Verified 2026-08-04 | Individual requests to the six bare slugs |
| 3 | The Gamma section serves 152 URLs | Verified 2026-08-04 | `gravitee-gamma/sitemap-pages.xml` |
| 4 | All 152 Gamma URLs return 200 | Verified 2026-08-04 | Per-URL requests, zero non-200 responses |
| 5 | 14 redirect entries exist in the 4.12 space file | Verified 2026-08-04 | `docs/gamma/4.12/.gitbook.yaml` lines 7 to 21 |
| 6 | The same 14 entries exist in the 4.13 space file | Verified 2026-08-04 | `docs/gamma/4.13/.gitbook.yaml` lines 7 to 21 |
| 7 | Each of the 14 sources returns 307 to the listed current target | Verified 2026-08-04 | Per-URL requests capturing each redirect location |
| 8 | The proposed space skeleton matches the existing configuration | Verified 2026-08-04 | `docs/gamma/4.12/.gitbook.yaml` lines 1 to 5 |
| 9 | The six modules are the top-level groups of the Gamma navigation | Verified 2026-08-04 | `docs/gamma/4.12/SUMMARY.md` group headings at lines 5, 40, 67, 83, 127, and 167 |
| 10 | Space YAML redirect targets must be real `.md` files in the same space | Verified 2026-06-10 | Platform-overview removal work (PR #1650), re-verify at execution |
| 11 | Repo-root YAML redirects never fire | Verified 2026-07-22 | `/ae` and `/alert-engine` returned 404 despite root entries |
| 12 | Auto-redirects cover editor moves and renames | Verified 2026-08-03 | 8 legacy URLs returned 307 with no explicit rule |
| 13 | Auto-redirects don't cover section removal, slug renames, or deletions | Verified 2026-08-03 | 14 legacy URLs returned 404 until PR #2124 |
| 14 | Published URLs follow the nav tree, not file paths | Verified 2026-08-03 | `edit-mcp-studio-composition.md` serving path |
| 15 | Bare `/apim` serves the default version and `/apim/4.12` returns 307 to it | Verified 2026-07-22 | Live requests, re-verify at flip |
| 16 | Site redirects support trailing wildcards, matched-text replacement, and CSV import of up to 500 rows | Documented by GitBook, not yet tested here | GitBook site redirects page, fetched 2026-08-04 |
| 17 | A site redirects API endpoint exists | Documented by GitBook, not yet tested here | GitBook API reference, found 2026-08-04 |
| 18 | Edge Management module content is the edge daemon surface | Verified 2026-08-04 | `docs/gamma/4.12/edge-management/` folder contents |
| 19 | The Gamma space is bound to `docs/gamma/4.12` with locked edit mode | Verified 2026-08-03 through the GitBook API | Re-verify at execution |
| 20 | 7 Gamma repo pages are hidden | Verified 2026-08-03 | Front-matter sweep, re-check at execution |
| 21 | `/edge-stack` page sitemap returns zero URLs | Verified 2026-08-04 | `edge-stack/sitemap-pages.xml`, enumerate that section another way before any removal decision |
| 22 | Destination candidates for the five legacy sections | Proposed, not verified | Open decisions 1 to 4 |
