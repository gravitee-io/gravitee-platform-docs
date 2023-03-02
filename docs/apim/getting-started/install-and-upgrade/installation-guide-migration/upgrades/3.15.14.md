# Breaking changes

## API key and JWT plans

The security chain (the internal process that selects the executable
plan for the incoming request and applies the related security rules)
parses all active plans to select and execute the relevant one.

**Prior to this version:**

-   The API key plan was executed if the request contained an API key.

-   The JWT plan was executed if the request contained a Bearer token.

**From this version:**

The security chain has been improved to select and execute plans more
efficiently. As a result, API keys and JWT plans are now only executed
if there is an active subscription related to the provided security
token. If there is no relevant subscription, the currently parsed plans
are not executed and the security chain moves to parse the next
available plans. The process continues until the security chain parses
plans related to the provided security token and these plans are
executed, or until all available plans are parsed without a match.

Specific examples of this change are provided in the table below:

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>API plans</p></td>
<td style="text-align: left;"><p>Request</p></td>
<td style="text-align: left;"><p>Prior to this version</p></td>
<td style="text-align: left;"><p>From this version</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>API key plan + Keyless plan</p></td>
<td style="text-align: left;"><p>Request contains an invalid API
key</p></td>
<td style="text-align: left;"><p>API key plan is executed = HTTP 401
unauthorized</p></td>
<td style="text-align: left;"><p>Keyless plan is executed</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>JWT plan 1 + JWT plan 2</p></td>
<td style="text-align: left;"><p>Request contains a Bearer token valid
for JWT plan 2</p></td>
<td style="text-align: left;"><p>JWT plan 1 is executed = HTTP 401
unauthorized</p></td>
<td style="text-align: left;"><p>JWT plan 2 is executed</p></td>
</tr>
</tbody>
</table>
