# Vale suggestion test page

```text
THROWAWAY TEST FILE - delete before merge.
Everything in this fenced block is ignored by Vale (BlockIgnores).

This file exercises every Vale behavior category so you can see all of
them on one PR:

  CATEGORY A - Commit-suggestion button via action:replace
    Microsoft.Contractions, docs.word-choice

  CATEGORY B - Commit-suggestion button via Vale.Terms message parse
    Vale.Terms (built-in vocab rule)

  CATEGORY C - Plain comment, "remove" action, NO button (conditional fix)
    Microsoft.Adverbs

  CATEGORY D - Plain comment, no fix at all, NO button
    Microsoft.We (rewrite needed), Microsoft.SentenceLength (no auto-fix),
    Vale.Repetition (built-in, ambiguous fix)
```

## Category B - Vale.Terms (button: api to API)

The api reference page documents every api endpoint in detail.

## Category A - Microsoft.Contractions (button: do not to don't)

If the gateway does not respond, do not retry the request immediately.

## Category A - docs.word-choice (button: lowercase to canonical)

Open the developer portal, check the alert engine, then visit gravitee.io.

## Category C - Microsoft.Adverbs (remove action, no button)

The gateway is very fast and really reliable in production.

## Category D - Microsoft.We (no fix, rewrite needed, no button)

We recommend that we secure the gateway before we expose it publicly.

## Category D - Vale.Repetition (built-in, no button)

Restart the the gateway after applying the configuration change.

## Category D - Microsoft.SentenceLength (no auto-fix, no button)

This sentence is intentionally written to be far longer than it really needs to be so that it comfortably exceeds the configured maximum sentence length and is flagged by the Microsoft sentence length rule without offering any automatic fix whatsoever.
