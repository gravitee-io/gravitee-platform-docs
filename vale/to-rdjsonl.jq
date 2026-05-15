# Converts `vale --output=JSON` into reviewdog rdjsonl (one diagnostic per line).
#
# A `suggestions` block is emitted (so GitHub renders the "Commit suggestion"
# button) only when a deterministic replacement is available:
#   1. Rules with `action: {name: replace}` (Microsoft.Contractions,
#      docs.word-choice, other substitution rules) -> use Action.Params[0].
#   2. Vale.Terms (built-in vocab rule, carries no action) -> parse the
#      replacement out of its fixed "Use 'X' instead of 'Y'." message.
# Advisory rules with no fixed replacement (Microsoft.SentenceLength,
# Microsoft.We, etc.) post as plain comments with no suggestion button.
#
# Vale Span is 1-based and inclusive on both ends; reviewdog Range.end is
# exclusive, so end.column = Span[1] + 1.

to_entries[]
| select(.value | type == "array")
| .key as $path
| .value[]
| ( {
      line:   .Line,
      scol:   .Span[0],
      ecol:   (.Span[1] + 1)
    } ) as $pos
| {
    message: "[\(.Check)] \(.Message)",
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
        then .Action.Params[0]
        elif (.Check == "Vale.Terms")
             and (.Message | test("^Use '[^']+' instead of '"))
        then (.Message | capture("^Use '(?<r>[^']+)' instead of '") | .r)
        else null
        end
      ) as $rep
      | if $rep == null
        then {}
        else { suggestions: [ {
                 range: {
                   start: { line: $pos.line, column: $pos.scol },
                   end:   { line: $pos.line, column: $pos.ecol }
                 },
                 text: $rep
               } ] }
        end
    )
