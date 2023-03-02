The JavaScript policy is not included by default. To use this policy,
you must download and install the plugin.

# Phases

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>onRequest</p></td>
<td style="text-align: left;"><p>onResponse</p></td>
<td style="text-align: left;"><p>onRequestContent</p></td>
<td style="text-align: left;"><p>onResponseContent</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>X</p></td>
<td style="text-align: left;"><p>X</p></td>
<td style="text-align: left;"><p>X</p></td>
<td style="text-align: left;"><p>X</p></td>
</tr>
</tbody>
</table>

# Description

You can use this policy to run [Javascript^](http://www.javascript.com/)
scripts at every stage of gateway processing.

# Phase - onRequest

As an example of what you can do in the **onRequest** phase, this script
stops the processing if the request contains a certain header.

    if (request.headers.containsKey('X-Gravitee-Break')) {
        result.state = State.FAILURE;
        result.code = 500
        result.error = 'Stopped processing due to X-Gravitee-Break header'
    } else {
        request.headers.set('X-Javascript-Policy', 'ok');
    }

In the **onRequest** phase you have access to the **request** object and
the **context** object.

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Object</p></td>
<td style="text-align: left;"><p>Property</p></td>
<td style="text-align: left;"><p>Type</p></td>
<td style="text-align: left;"><p>Description</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>id</p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>transactionId</p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>uri</p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>path</p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>pathInfo</p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>contextPath</p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>parameters</p></td>
<td style="text-align: left;"><p>multivalue map</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>pathParameters</p></td>
<td style="text-align: left;"><p>multivalue map</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>headers</p></td>
<td style="text-align: left;"><p>iterable map &lt;string,
string&gt;</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>method</p></td>
<td style="text-align: left;"><p>enum</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>version</p></td>
<td style="text-align: left;"><p>enum</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>timestamp</p></td>
<td style="text-align: left;"><p>long</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>remoteAddress</p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>localAddress</p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>scheme</p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>sslSession</p></td>
<td style="text-align: left;"><p>javax.net.ssl.SSLSession</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>request</p></td>
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p><a
href="#metricsobject">object</a></p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
</tbody>
</table>

The **context** object doesn’t have known properties as such, it
contains the attributes of the execution environment. And you can add
some yourself too. For example, this could be the first line of your
**onRequest** script:

    context.setAttribute('custom-policy-start',Date.now());

That probably doesn’t look all that exciting, but wait until the
**onResponse** script and you’ll see! The **context** object gives you
access to the following methods:

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Object</p></td>
<td style="text-align: left;"><p>Method</p></td>
<td style="text-align: left;"><p>Description</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>context</p></td>
<td style="text-align: left;"><p>Object getAttribute(String)</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>context</p></td>
<td style="text-align: left;"><p>void setAttribute(String,
Object)</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>context</p></td>
<td style="text-align: left;"><p>void removeAttribute(String)</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>context</p></td>
<td style="text-align: left;"><p>Map&lt;String, Object&gt;
getAttributes()</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
</tbody>
</table>

# Phase - onRequestContent

In the **onRequestContent** phase you have access to the **content**
object, also known as the [request
body^](https://dzone.com/articles/rest-api-path-vs-request-body-parameters).
You can modify this object.

As an example, assuming the following request body:

    [
        {
            "age": 32,
            "firstname": "John",
            "lastname": "Doe"
        }
    ]

Then you can do the following:

    var content = JSON.parse(request.content);
    content[0].firstname = 'Hacked ' + content[0].firstname;
    content[0].country = 'US';

    JSON.stringify(content);

And the request body being passed to the API would be:

    [
        {
            "age": 32,
            "firstname": "Hacked John",
            "lastname": "Doe",
            "country": "US"
        }
    ]

When working with scripts on onRequestContent phase, the last
instruction of the script **must be** the new body content that would be
returned by the policy.

# Phase - onResponse

In the **onResponse** phase you have access to the **request**, the
**response** and the **context** object.

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Object</p></td>
<td style="text-align: left;"><p>Property</p></td>
<td style="text-align: left;"><p>Type</p></td>
<td style="text-align: left;"><p>Description</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>response</p></td>
<td style="text-align: left;"><p>status</p></td>
<td style="text-align: left;"><p>int</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>response</p></td>
<td style="text-align: left;"><p>reason</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>response</p></td>
<td style="text-align: left;"><p>headers</p></td>
<td style="text-align: left;"><p>iterable map &lt;string,
string&gt;</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
</tbody>
</table>

As an example of what you can do in the **onResponse** phase, this
script modifies the headers. And it uses the custom **context**
attribute you set in the **onRequest** phase too:

    response.headers.remove('Server');
    response.headers.set('Server', 'Powered by Gravitee');
    response.headers.set('X-Time-Elapsed', String(Date.now() - context.getAttribute('custom-policy-start')));

# Phase - onResponseContent

In the **onResponseContent** phase you have access to the **content**
object, also known response message. You can modify this object.

As an example, assume that you sent the request body modified in the
**onRequestContent** phase to an **echo** API. You can do the following:

    var content = JSON.parse(response.content);
    content[0].firstname = content[0].firstname.substring(7);
    delete content[0].country;
    JSON.stringify(content);

And the reponse message would be:

    [
        {
            "age": 32,
            "firstname": "John",
            "lastname": "Doe"
        }
    ]

When working with scripts on onResponseContent phase, the last
instruction of the script **must be** the new body content that would be
returned by the policy.

# Reference - Metrics <span id="metricsobject"></span>

It is highly advisable to use the link:{% link
pages/apim/3.x/policy-reference/policy-metrics-reporter.adoc %}\[Metrics
Reporter\] in order to manage the metrics. However, the request object
does contain a **metrics** object.

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Object</p></td>
<td style="text-align: left;"><p>Property</p></td>
<td style="text-align: left;"><p>Type</p></td>
<td style="text-align: left;"><p>Description</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>api</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>ID of the API</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>apiResponseTimeMs</p></td>
<td style="text-align: left;"><p>long</p></td>
<td style="text-align: left;"><p>Response time spend to call the backend
upstream</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>application</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>ID of the consuming
application</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>endpoint</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>errorKey</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>Key of the error if the policy chain is
failing</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>host</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>Host header value</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>httpMethod</p></td>
<td style="text-align: left;"><p>enum</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>localAddress</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>log</p></td>
<td style="text-align: left;"><p>object</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>mappedPath</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>message</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>path</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>plan</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>ID of the plan</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>proxyLatencyMs</p></td>
<td style="text-align: left;"><p>long</p></td>
<td style="text-align: left;"><p>Latency of the gateway to apply
policies</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>proxyResponseTimeMs</p></td>
<td style="text-align: left;"><p>long</p></td>
<td style="text-align: left;"><p>Global response time to process and
respond to the consumer</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>remoteAddress</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>requestContentLength</p></td>
<td style="text-align: left;"><p>long</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>requestId</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>responseContentLength</p></td>
<td style="text-align: left;"><p>long</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>securityToken</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>securityType</p></td>
<td style="text-align: left;"><p>enum</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>status</p></td>
<td style="text-align: left;"><p>int</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>subscription</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>ID of the subscription</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>tenant</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>gateway tenant value</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>transactionId</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>uri</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>user</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>End-user doing the call (in case of
OAuth2 / JWT / Basic Auth)</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>userAgent</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>Value of the user-agent header</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>metrics</p></td>
<td style="text-align: left;"><p>zone</p></td>
<td style="text-align: left;"><p>String</p></td>
<td style="text-align: left;"><p>Gateway zone</p></td>
</tr>
</tbody>
</table>

The metrics object changes in the different processing phases and some
properties may not make sense in certain phases!
