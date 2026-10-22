---
hidden: false
noIndex: false
description: The IP, decimal, datetime, and duration functions of GAPL, the string formats they accept, and the methods of the values they build.
---

# Extension functions

Four functions build values that GAPL has no literal for. Each takes a string and returns a value with its own methods:

| Function | Builds | Example |
|----------|--------|---------|
| `ip("...")` | An IP address or an address range | `ip("10.0.0.0/8")` |
| `decimal("...")` | A decimal number with up to four fractional digits | `decimal("0.75")` |
| `datetime("...")` | An instant in time | `datetime("2026-06-30T17:00:00Z")` |
| `duration("...")` | A length of time | `duration("1h30m")` |

The argument can be any expression that gives a string, such as an attribute or a context field:

```text
ip(context.clientIp).isInRange(ip(resource.allowedNetwork))
```

A method is called on the value with `.`, such as `a.isInRange(b)`. It can also be called as a function with the value as its first argument, such as `isInRange(a, b)`.

A string that doesn't match the format of its function is an error, and so is a function or a method name that doesn't exist. In both cases the statement is skipped. Neither is caught when you save. For what skipping means, see [How statements are evaluated](evaluation.md).

## `ip`

`ip("...")` accepts the following formats:

| Format | Example |
|--------|---------|
| IPv4 address | `ip("192.168.1.10")` |
| IPv4 range, in CIDR notation | `ip("10.0.0.0/8")` |
| IPv6 address | `ip("2001:db8::1")` |
| IPv6 range, in CIDR notation | `ip("2001:db8::/32")` |

An IPv4 address has four decimal parts from `0` to `255`, without leading zeros: `ip("010.0.0.1")` is an error. The prefix length is `0` to `32` for IPv4 and `0` to `128` for IPv6, also without leading zeros. An IPv6 address that embeds an IPv4 address, such as `::ffff:10.0.0.1`, isn't accepted. Host names aren't accepted.

An IP value has the following methods:

| Method | Returns | Result |
|--------|---------|--------|
| `a.isInRange(r)` | `Bool` | `true` when the address `a`, or every address of the range `a`, lies in the range `r`. An IPv4 value is never in an IPv6 range, and an IPv6 value is never in an IPv4 range |
| `a.isIpv4()` | `Bool` | `true` for an IPv4 address or range |
| `a.isIpv6()` | `Bool` | `true` for an IPv6 address or range |
| `a.isLoopback()` | `Bool` | `true` when `a` lies in `127.0.0.0/8` or is `::1` |
| `a.isMulticast()` | `Bool` | `true` when `a` lies in `224.0.0.0/4` or `ff00::/8` |

```text
ip(principal.lastIp).isInRange(ip("10.0.0.0/8"))
!ip(context.clientIp).isLoopback()
```

## decimal

`decimal("...")` accepts an optional `-`, digits, a `.`, and one to four digits: `decimal("12.5")`, `decimal("-0.0025")`. A whole number needs a fractional part, so write `decimal("12.0")`, not `decimal("12")`. Exponents, such as `1e3`, aren't accepted. The range is from `-922337203685477.5808` to `922337203685477.5807`.

Decimals compare with methods, not with `<` or `>`. `==` and `!=` work as for any value.

A decimal has the following methods:

| Method | Returns | Result |
|--------|---------|--------|
| `a.lessThan(b)` | `Bool` | `true` when `a < b` |
| `a.lessThanOrEqual(b)` | `Bool` | `true` when `a <= b` |
| `a.greaterThan(b)` | `Bool` | `true` when `a > b` |
| `a.greaterThanOrEqual(b)` | `Bool` | `true` when `a >= b` |

```text
decimal(resource.riskScore).lessThan(decimal("0.7"))
```

## datetime

`datetime("...")` accepts the following formats:

| Format | Example |
|--------|---------|
| A date, read as midnight UTC | `datetime("2026-06-30")` |
| A date and a time in UTC | `datetime("2026-06-30T17:00:00Z")` |
| A date and a time with an offset | `datetime("2026-06-30T19:00:00+02:00")`, `datetime("2026-06-30T19:00:00+0200")` |

The time is `hh:mm`, optionally followed by `:ss`, and then by `.` and exactly three digits of milliseconds, such as `17:00:00.250`. A time must be followed by `Z` or by an offset. The separator between the date and the time is `T`. The following strings are errors:

| String | Reason |
|--------|--------|
| `2026-06-30T17:00:00` | No zone |
| `2026-06-30 17:00:00Z` | A space |
| `2026-06-30T17:00:00.123456Z` | Six fractional digits |
| `2026-06-30T17:00:00z` | A lowercase `z` |

Datetimes compare with `<`, `<=`, `>`, `>=`, `==`, and `!=`, by the instant they stand for.

A datetime has the following methods:

| Method | Returns | Result |
|--------|---------|--------|
| `t.offset(d)` | `datetime` | `t` moved by the duration `d`, forward or, for a negative `d`, back |
| `t.durationSince(u)` | `duration` | The time from `u` to `t`, negative when `u` is later |
| `t.toDate()` | `datetime` | Midnight UTC of the UTC day of `t` |
| `t.toTime()` | `duration` | The time elapsed since midnight UTC on the UTC day of `t` |

`toDate()` and `toTime()` always work in UTC, whatever the offset of the string: `datetime("2026-06-30T10:00:00+02:00").toTime()` is `duration("8h")`. Write time windows in UTC:

```text
datetime(context.requestTime).toTime() >= duration("7h") && datetime(context.requestTime).toTime() < duration("15h")
datetime(resource.expiresAt) > datetime(context.requestTime)
datetime(context.requestTime).durationSince(datetime(principal.passwordChangedAt)) < duration("90d")
```

## duration

`duration("...")` accepts one or more of the following parts, in this order and without spaces, with an optional `-` in front:

| Part | Unit |
|------|------|
| `<n>d` | Days |
| `<n>h` | Hours |
| `<n>m` | Minutes |
| `<n>s` | Seconds |
| `<n>ms` | Milliseconds |

For example: `duration("90s")`, `duration("1h30m")`, `duration("2d12h")`, `duration("-15m")`, `duration("500ms")`. Each `<n>` is a whole number. The following strings are errors:

| String | Reason |
|--------|--------|
| `1.5h` | A fraction |
| `1h 30m` | A space |
| `30m1h` | The wrong order |
| `30ns`, `10us` | Units that don't exist |
| `PT1H` | ISO 8601 notation |

Durations compare with `<`, `<=`, `>`, `>=`, `==`, and `!=`.

A duration has the following methods:

| Method | Returns | Result |
|--------|---------|--------|
| `d.toMilliseconds()` | `Long` | The length in milliseconds |
| `d.toSeconds()` | `Long` | The length in whole seconds |
| `d.toMinutes()` | `Long` | The length in whole minutes |
| `d.toHours()` | `Long` | The length in whole hours |
| `d.toDays()` | `Long` | The length in whole days |

The whole-unit methods drop the remainder: `duration("1h59m").toHours()` is `1`.
