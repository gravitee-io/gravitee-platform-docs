# Converts `vale --output=JSON` into reviewdog rdjsonl (one diagnostic per line).
#
# A `suggestions` block (GitHub's one-click "Commit suggestion" button) is
# emitted only when Vale gives a deterministic replacement:
#   1. action {name:"replace"}            -> Action.Params[0]
#        Microsoft.Contractions, docs.word-choice, other substitution rules.
#   2. Vale.Terms (built-in vocab, no action) -> parse "Use 'X' instead of 'Y'."
#   3. action {name:"edit", params:["truncate", SEP]} -> first SEP-segment of
#        Match. Vale.Repetition: Match "the the", SEP " " -> "the".
#   4. action {name:"remove"}             -> delete the word (empty text). The
#        range is widened one column left to also consume the preceding space
#        (an adverb is almost always preceded by a space), guarded so it never
#        underflows column 1. Microsoft.Adverbs and any other remove rule.
#   5. docs.Spelling carrying a `Suggestion` field. Vale's JSON omits spelling
#        candidates, so vale/add-spelling-suggestions.py augments each
#        docs.Spelling alert with a `Suggestion` field upstream of this jq.
#        When the helper finds no plausible candidate, the field is absent
#        and the alert falls through to a plain comment.
#
# Rules with no deterministic fix (Microsoft.We, Microsoft.SentenceLength) and
# Microsoft.Spacing (mechanical fix exists but corrupts identifiers like
# "Vale.Terms" -> "Vale. Terms") post as plain comments, no button.
#
# Vale Span is 1-based and inclusive on both ends; reviewdog Range.end is
# exclusive, so end.column = Span[1] + 1.

to_entries[]
| select(.value | type == "array")
| .key as $path
| .value[]
| ( {
      line: .Line,
      scol: .Span[0],
      ecol: (.Span[1] + 1)
    } ) as $pos
| {
    message: ( "[\(.Check)] \(.Message)"
               + ( if (.Link // "") != "" then " (\(.Link))" else "" end ) ),
    location: {
      path: $path,
      range: {
        start: { line: $pos.line, column: $pos.scol },
        end:   { line: $pos.line, column: $pos.ecol }
      }
    },
    severity: ( .Severity
                | if   . == "error"   then "ERROR"
                  elif . == "warning" then "WARNING"
                  else "INFO" end ),
    source: { name: "vale", url: "https://vale.sh" },
    code: ( { value: .Check }
            + ( if (.Link // "") != "" then { url: .Link } else {} end ) )
  }
  + (
      ( if   (.Action.Name == "replace") and ((.Action.Params // []) | length) > 0
        then { text: .Action.Params[0], s: $pos.scol, e: $pos.ecol }

        elif (.Check == "Vale.Terms")
             and (.Message | test("^Use '[^']+' instead of '"))
        then { text: (.Message | capture("^Use '(?<r>[^']+)' instead of '") | .r),
                s: $pos.scol, e: $pos.ecol }

        elif (.Action.Name == "edit")
             and ((.Action.Params // []) | length >= 2)
             and (.Action.Params[0] == "truncate")
        then ( .Action.Params[1] as $sep
               | { text: ((.Match // "") | split($sep) | .[0]),
                   s: $pos.scol, e: $pos.ecol } )

        elif (.Action.Name == "remove")
        then { text: "",
                s: (if $pos.scol > 1 then $pos.scol - 1 else $pos.scol end),
                e: $pos.ecol }

        elif (.Check == "docs.Spelling")
             and ((.Suggestion // "") != "")
        then { text: .Suggestion, s: $pos.scol, e: $pos.ecol }

        else null
        end
      ) as $sug
      | if $sug == null
        then {}
        else { suggestions: [ {
                 range: {
                   start: { line: $pos.line, column: $sug.s },
                   end:   { line: $pos.line, column: $sug.e }
                 },
                 text: $sug.text
               } ] }
        end
    )
