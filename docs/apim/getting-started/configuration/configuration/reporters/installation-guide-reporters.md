Reporters are designed to record a variety of events occurring in the
gateway, to a variety of outputs and formats, in their order of
occurrence. This enables you to manage this data using a solution of
your choice.

The following event types are supported.

# Event types

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Type</p></td>
<td style="text-align: left;"><p>Description</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>request</code></p></td>
<td style="text-align: left;"><p>This event type provides common request
and response metrics, such as response time, application, request ID,
and more.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>log</code></p></td>
<td style="text-align: left;"><p>This event type provides more detailed
request and response metrics. It is reported when logging has been
enabled at the API level.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>healthcheck</code></p></td>
<td style="text-align: left;"><p>This event type allows for healthcheck
events to be reported when a healthcheck endpoint has been configured
and enabled on an API.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>node</code></p></td>
<td style="text-align: left;"><p>This event type provides some system
and JVM metrics for the node Gravitee is running on.</p></td>
</tr>
</tbody>
</table>

# Available Reporters

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Type</p></td>
<td style="text-align: left;"><p>Bundled</p></td>
<td style="text-align: left;"><p>Default</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Elasticsearch</p></td>
<td style="text-align: left;"><p>✓</p></td>
<td style="text-align: left;"><p>✓</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>File</p></td>
<td style="text-align: left;"><p>✓</p></td>
<td style="text-align: left;"><p>×</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>TCP</p></td>
<td style="text-align: left;"><p>✓</p></td>
<td style="text-align: left;"><p>×</p></td>
</tr>
</tbody>
</table>

# Configuring Reporters

## Elasticsearch Reporter

Configuration details for the elasticsearch reporter are available in
the link:{{
*/apim/3.x/apim\_installguide\_repositories\_elasticsearch.html* |
relative\_url }}\[Elasticsearch Repository\] documentation.

## File Reporter

### Configuration Parameters

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Parameter name</p></td>
<td style="text-align: left;"><p>Description</p></td>
<td style="text-align: left;"><p>Default value</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>enabled</code></p></td>
<td style="text-align: left;"><p>This setting determines whether the
file reporter should be started or not. The default value is
<code>false</code>.</p></td>
<td style="text-align: left;"><p>false</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>fileName</code></p></td>
<td style="text-align: left;"><p>The path events should be written to.
Use the <code>%s-yyyy_mm_dd</code> pattern to create one file per event
type on a daily basis.</p></td>
<td
style="text-align: left;"><p><strong>#{systemProperties[<em>gravitee.home</em>]}/metrics/%s-yyyy_mm_dd}</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>output</code></p></td>
<td style="text-align: left;"><p>Output file type - json, message_pack,
elasticsearch, csv.</p></td>
<td style="text-align: left;"><p><strong>json</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>flushInterval</code></p></td>
<td style="text-align: left;"><p>File flush interval (in ms).</p></td>
<td style="text-align: left;"><p><strong>1000</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>retainDays</code></p></td>
<td style="text-align: left;"><p>The number of days to retain files
before deleting one.</p></td>
<td style="text-align: left;"><p><strong>0 (to retain
forever)</strong></p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p><code>&lt;EVENT_TYPE&gt;.exclude</code></p></td>
<td style="text-align: left;"><p>Fields to exclude from the output.
Available for <code>json</code> and <code>message_pack</code> outputs
only.</p></td>
<td style="text-align: left;"><p><strong>none</strong></p></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p><code>&lt;EVENT_TYPE&gt;.include</code></p></td>
<td style="text-align: left;"><p>Fields to include in the output.
Available for <code>json</code> and <code>message_pack</code> outputs
and only if excludes have been defined.</p></td>
<td style="text-align: left;"><p><strong>none</strong></p></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p><code>&lt;EVENT_TYPE&gt;.rename</code></p></td>
<td style="text-align: left;"><p>Fields to rename when writing the
output. Available for <code>json</code> and <code>message_pack</code>
outputs only.</p></td>
<td style="text-align: left;"><p><strong>none</strong></p></td>
</tr>
</tbody>
</table>

&lt;EVENT\_TYPE&gt; refers to the kind of event reported by the gateway
and can be either `request`, `log`, `node` or `healthcheck`. Fields
referenced as `exclude`, `include` and `rename` items all support
[jsonPath](https://github.com/json-path/JsonPath) for accessing nested
elements.

### Example

The configuration example below excludes all fields from the request
JSON file except the `api` and `application` fields, renames the
`application` field to `app`, and excludes `log`, `node`, and
`healthcheck` events from being reported.

    reporters:
      file:
        enabled: true
        fileName: ${gravitee.home}/metrics/%s-yyyy_mm_dd
        output: json
        request:
          exclude:
            - "*"
          include:
            - api
            - application
          rename:
            application: app
        log:
          exclude: *
        node:
          exclude: *
        healthcheck:
          exclude: *

## TCP Reporter

### Configuration Parameters

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Parameter name</p></td>
<td style="text-align: left;"><p>Description</p></td>
<td style="text-align: left;"><p>Default value</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>enabled</code></p></td>
<td style="text-align: left;"><p>This setting determines whether the TCP
reporter should be started or not. The default value is
<code>false</code>.</p></td>
<td style="text-align: left;"><p>false</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>output</code></p></td>
<td style="text-align: left;"><p>Format of the data written to the TCP
socket - json, message_pack, elasticsearch, csv.</p></td>
<td style="text-align: left;"><p><strong>json</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>host</code></p></td>
<td style="text-align: left;"><p>The TCP host where the event should be
published. This can be a valid host name or an IP address.</p></td>
<td style="text-align: left;"><p><strong>localhost</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>port</code></p></td>
<td style="text-align: left;"><p>The TCP port used to connect to the
host.</p></td>
<td style="text-align: left;"><p><strong>8123</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>connectTimeout</code></p></td>
<td style="text-align: left;"><p>Maximum time allowed to establish the
TCP connection in milliseconds.</p></td>
<td style="text-align: left;"><p><strong>10000</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>reconnectAttempts</code></p></td>
<td style="text-align: left;"><p>This setting determines how many times
the socket should try to establish a connection in case of
failure.</p></td>
<td style="text-align: left;"><p><strong>10</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>reconnectInterval</code></p></td>
<td style="text-align: left;"><p>Time (in milliseconds) between socket
connection attempts.</p></td>
<td style="text-align: left;"><p><strong>500</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>retryTimeout</code></p></td>
<td style="text-align: left;"><p>If the max reconnect attempts have been
reached, this setting determines how long (in milliseconds) the reporter
should wait before trying to connect again.</p></td>
<td style="text-align: left;"><p><strong>5000</strong></p></td>
</tr>
</tbody>
</table>

### Example

The following example uses the same configuration as the previous
example above, however it writes the events to a TCP socket instead of a
file.

    reporters:
      tcp:
        enabled: true
        host: localhost
        port: 9001
        output: json
        request:
          exclude:
            - "*"
          include:
            - api
            - application
          rename:
            application: app
        log:
          exclude: *
        node:
          exclude: *
        healthcheck:
          exclude: *
