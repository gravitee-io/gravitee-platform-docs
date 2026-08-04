# Git hooks

## Install

Run this once, from the repository root:

```bash
git config core.hooksPath .githooks
```

Git doesn't install hooks automatically when you clone, so every contributor runs
this themselves. To confirm it's active:

```bash
git config core.hooksPath   # prints .githooks
```

## commit-msg

Blocks a commit whose message contains a customer name, a contact name, an email
address, or an internal tool console URL. This is critical rule 36, and SOC 2 and
GDPR make it a hard gate: commit messages are public and effectively permanent, so
a leak can't be retracted.

What it rejects, and what to write instead:

| Rejected | Write instead |
|---|---|
| `Reported by Jane Doe (customer: Acme Corp).` | `Reported by a customer (DOC-1234).` |
| `Requested by Jane Doe` | `Requested by a customer (DOC-1234).` |
| `Acme Corp asked for this` | `A customer asked for this (DOC-1234).` |
| `Portal settings (Acme ticket): ...` | `Portal settings (customer ticket): ...` |
| `Supported versions (ACME request, TT-1 context)` | `Supported versions (customer request, TT-1 context)` |
| `Proxy addition (super urgent for Acme-Group)` | `Proxy addition (urgent for a customer, DOC-1234)` |
| `jane.doe@acme.com hit this bug` | `A customer hit this bug (DOC-1234).` |
| `https://<org>.zendesk.com/agent/tickets/12345` | `Zendesk #12345` |
| `https://<org>.slack.com/archives/C0.../p17...` | Describe the source, or cite the ticket. |

The middle three matter most: a bare company name next to "ticket", "request", or
"feedback" carries no marker word, so it's the form that slips through review.

The ticket ID is the traceability link. Jira and Zendesk are where the customer
association belongs, not the git history.

Email addresses inside standard git trailers (`Co-authored-by:`, `Signed-off-by:`,
`Reviewed-by:`, and similar) are allowed, since those are how git records authorship.

### Bypassing

`git commit --no-verify` skips the hook. Use it only when you're certain the match
is a false positive. CI runs the identical script on every pull request, so a
bypassed commit is caught before merge rather than after.

### False positives

The check is tuned against this repository's history: it flags 2 of the most recent
200 commits, and both of those are genuine leaks. If you hit a false positive, fix
the check rather than widening it to the point of uselessness, and never delete a
rule to get a commit through.
