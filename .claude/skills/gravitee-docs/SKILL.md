---
name: gravitee-docs
description: Search Gravitee product documentation (APIM, AM, GKO, Gamma, Gravitee Cloud, EE) scoped to a specific product and version, or resolve a documentation.gravitee.io link or repo path to the exact file. Auto-detects the latest version when none is given. Use whenever the user asks to look up, search, or check docs for a Gravitee product/version.
---

# Gravitee docs search

**Mirror — don't edit this copy.** The source of truth is
`documentation-codebase/ai-tools/gravitee-docs-skill.md`, where the
Documentation team maintains it alongside the pipelines that reference it.
This copy lives here so the skill loads automatically for anyone with
`gravitee-platform-docs` cloned, with nothing to install. Change the
`documentation-codebase` file, then re-copy the body into this one — an edit
made only here is invisible to the team and drifts silently.

Scopes a search or a file lookup to one product/version within
`gravitee-platform-docs`, instead of searching or reading that whole repo
unscoped. All paths below are relative to this repo's root; resolve its
checkout with `git rev-parse --show-toplevel` rather than hardcoding an
absolute path.

Search itself runs through the local RAG stack (`gravitee-local-tooling`),
via the `rag_search` MCP tool (`mcp__vectordb__rag_search` if connected) or
`curl -s -X POST http://localhost:8000/search` with the same JSON body. Call
`rag_health` first and treat a `mock` `embedding_backend` as untrustworthy,
same as `verify-doc-pipeline.md` Step 2 does. If neither the MCP tool nor
the API is reachable, that stack isn't set up on this machine — fall back
to `grep -ril` over the resolved directory as a rough substitute, and say so
rather than silently returning nothing.

## Product mapping

| User says | Folder | Versioned? |
|---|---|---|
| apim, api management | `apim` | yes |
| am, access management | `am` | yes |
| gko, kubernetes operator, gravitee kubernetes operator | `gko` | yes |
| gamma | `gamma` | yes |
| gravitee-cloud, cloud | `gravitee-cloud` | no |
| ee, enterprise edition | `ee` | no |

Gamma is versioned, and has been since its first release — `docs/gamma/`
contains version folders (`4.12`, `4.13`, …) and no pages at the product
root. Treat it exactly like `apim`, `am`, and `gko`.

`blackbird`, `edge-stack`, and `telepresence` exist in `docs/` but are
excluded from the RAG index — say so if asked about them, don't silently
search anyway.

## Given a doc URL or a file path instead of a product name

Public doc URLs (`https://documentation.gravitee.io/<product>/<version>/<rest...>`)
and `gravitee-platform-docs` paths (`docs/<product>/<version>/<rest...>`)
map 1:1 onto that repo's folder structure — the URL path *is* the file
path, just without the `docs/` prefix or the file extension. When given a
link or a path, don't go through the alias table or latest-detection below
— parse it directly:

1. Strip the scheme/host (for a URL) or the `docs/` prefix (for a path), and
   any trailing `#anchor` / `?query`.
2. Split into segments. Segment 1 is the product.
3. If segment 2 matches `^\d+\.\d+$`, it's the version, and everything after
   it is the in-version subpath. If it doesn't match (unversioned product),
   there's no version — everything from segment 2 onward is the subpath.
4. This gives an exact candidate file:
   `docs/<product>/[<version>/]<subpath>.md` (try `.adoc` if `.md` 404s, and
   check for a `README.md` if the path looks like a directory rather than a
   page).
5. **Read that file directly** rather than searching — a link points at one
   specific page, so there's no need for retrieval, and no dependency on the
   RAG stack being set up at all. Only fall back to a `path_prefix` search
   scoped to that product/version if the exact file isn't there (e.g. the
   page was renamed or moved since the link was generated). This is also
   the fastest way to satisfy `verify-doc-pipeline.md` Step 1 ("read the
   target file") when you were handed a live doc link instead of a repo
   path.

Example: `https://documentation.gravitee.io/apim/4.11/hybrid-installation-and-configuration-guides/next-gen-cloud/docker/docker-cli`
→ product `apim`, version `4.11`, file
`docs/apim/4.11/hybrid-installation-and-configuration-guides/next-gen-cloud/docker/docker-cli.md`.

## Resolving the version (when no link/path was given)

1. **Explicit version given** (e.g. "apim 4.9") → use it as-is.
2. **"all versions" / "any version" / "across versions" requested** → omit
   the version segment entirely (prefix stops at the product folder), so
   the prefix match naturally spans every version.
3. **No version mentioned at all** → default to the latest version. Resolve
   it by listing the numeric subfolders and taking the highest via version
   sort (do NOT use plain alphabetical sort — `4.9` must sort below `4.10`):

   ```
   ls <gravitee-platform-docs-root>/docs/<product> | grep -E '^[0-9]' | sort -V | tail -1
   ```

   This also naturally skips the `archive/` folder under `docs/apim/` since
   it isn't purely numeric.

4. **Unversioned product** (gravitee-cloud, ee) → no version step,
   prefix stops at the product folder.

## Building the search

Given a resolved product/version, construct:

- `source`: `repo/gravitee-platform-docs`
- `path_prefix`:
  - versioned + specific version: `docs/<product>/<version>/`
  - versioned + all-versions request: `docs/<product>/`
  - unversioned product: `docs/<product>/`
  - no product named at all (general question): omit `path_prefix`,
    `source` filter only

Example call:

```json
{
  "query": "rate limiting policy",
  "source": "repo/gravitee-platform-docs",
  "path_prefix": "docs/apim/4.13/",
  "hybrid": true,
  "limit": 8
}
```

## Presenting results

- State which product/version was actually searched, especially when the
  version was auto-detected rather than named — don't leave that implicit.
- Show file paths as clickable references, not raw JSON dumps.
- These are RAG hits for orientation, not verified fact — if you're about
  to act on a result (not just answering a question), open the actual file
  to confirm before relying on it, same as the rest of this team's
  AI-assisted workflows.
