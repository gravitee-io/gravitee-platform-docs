# Dashboard View State URL Encoding Specification

## URL State Encoding

Dashboard filter and time range state is encoded in the `q` query parameter using a unified, version-controlled format. The `v` parameter indicates the encoding version (currently `1`).

**Example Encoded URL:**

```
?q={"filter":[{"field":"API","operator":"EQ","value":"id-1"}],"time_range":{"type":"relative","period":"1h"}}&v=1
```

**Decoded Structure:**

```json
{
 "filter": [
 {
 "field": "API",
 "operator": "EQ",
 "value": "id-1"
 }
 ],
 "time_range": {
 "type": "relative",
 "period": "1h"
 }
}
```

### Encoding Rules

| Condition | Encoding Behavior |
|:----------|:------------------|
| Single-value filter (`values.length === 1`) | Encoded as `value: string` |
| Multi-value filter (`values.length > 1`) | Encoded as `value: string[]` |
| Filter with `label` or `valueLabels` | Labels are **never** included in encoded output |
| No filters and default timeframe (`5m`) | `encodeViewState` returns `null` (no `q` parameter in URL) |
| Invalid relative period | Ignored during encoding; defaults to `5m` during decoding |
| Absolute timeframe with `from` or `to` missing | Treated as invalid; defaults to `5m` during decoding |

### Decoding Rules

| Input Condition | Decoding Behavior |
|:----------------|:------------------|
| `q` is `null` or `v !== '1'` | Returns default: `{ conditions: [], timeframe: { period: '5m', from: null, to: null } }` |
| Invalid JSON in `q` | Logs warning; returns defaults |
| Filter entry missing `field` or `operator` | Entry is filtered out |
| `label` absent in encoded filter | Decoded `label` defaults to `field` value |
| `time_range` absent | Decoded `timeframe` defaults to `{ period: '5m', from: null, to: null }` |
| Invalid relative period in `time_range` | Decoded `timeframe` defaults to `{ period: '5m', from: null, to: null }` |

### Valid Relative Periods

`1m`, `5m`, `1h`, `1d`, `1w`, `1M`

### Time Range Encoding Reference

| Timeframe Type | Condition | Encoded Format |
|:---------------|:----------|:---------------|
| Relative | `period !== '5m'` and period is valid | `{ type: 'relative', period: string }` |
| Absolute | `period === 'custom'` and `from`, `to` are non-null | `{ type: 'absolute', from: number, to: number }` |
| Default (`5m`) | `period === '5m'` | Omitted from payload (`time_range` undefined) |

### Restrictions

- Filter labels (`label`, `valueLabels`) are **not** persisted in URL encoding. Decoded filters use `field` as the fallback label. Consumers must re-attach display labels after decoding if needed.
- `decodeViewState` only processes payloads with `v === '1'`. Future schema versions will require explicit version handling.
- Malformed JSON in the `q` parameter logs a warning and returns default state. No error is surfaced to the user.
- If `payload.filter` is not an array (e.g., object, string, null), it is silently ignored and treated as an empty filter set.
