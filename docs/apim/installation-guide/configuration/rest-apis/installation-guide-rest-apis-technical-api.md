The APIM API component comes with its own internal API, for monitoring
and retrieving technical information about the component.

# Configuration

You need to enable the API as a service in the `gravitee.yml` file and
update any other required configuration.

    services:
      core:
        http:
          enabled: true
          port: 18083
          host: localhost
          authentication:
            type: basic
            users:
              admin: adminadmin

enabled  
Whether the service is enabled (default `true`).

port  
The port the service listens on (default `{node_port}`). You must ensure
you use a port which is not already in use by another APIM component.

host  
The host (default `localhost`).

authentication.type  
Authentication type for requests: `none` if no authentication is
required or `basic` (default `basic`).

authentication.users  
A list of `user: password` combinations. Only required if authentication
type is `basic`.

# Endpoints

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Operation</p></td>
<td style="text-align: left;"><p>Description</p></td>
<td style="text-align: left;"><p>Example</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>GET /_node</code></p></td>
<td style="text-align: left;"><p>Gets generic node information</p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb1"><pre
class="sourceCode json"><code class="sourceCode json"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a><span class="er">HTTP/1.1</span> <span class="er">200</span> <span class="er">OK</span></span>
<span id="cb1-2"><a href="#cb1-2" aria-hidden="true" tabindex="-1"></a><span class="er">Content-Type:</span> <span class="er">application/json</span></span>
<span id="cb1-3"><a href="#cb1-3" aria-hidden="true" tabindex="-1"></a><span class="fu">{</span></span>
<span id="cb1-4"><a href="#cb1-4" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;id&quot;</span><span class="fu">:</span> <span class="st">&quot;a70b9fd9-9deb-4ccd-8b9f-d99deb6ccd32&quot;</span><span class="fu">,</span></span>
<span id="cb1-5"><a href="#cb1-5" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;metadata&quot;</span><span class="fu">:</span> <span class="fu">{},</span></span>
<span id="cb1-6"><a href="#cb1-6" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;name&quot;</span><span class="fu">:</span> <span class="st">&quot;Gravitee.io - Management API&quot;</span><span class="fu">,</span></span>
<span id="cb1-7"><a href="#cb1-7" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;version&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb1-8"><a href="#cb1-8" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;BUILD_ID&quot;</span><span class="fu">:</span> <span class="st">&quot;309&quot;</span><span class="fu">,</span></span>
<span id="cb1-9"><a href="#cb1-9" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;BUILD_NUMBER&quot;</span><span class="fu">:</span> <span class="st">&quot;309&quot;</span><span class="fu">,</span></span>
<span id="cb1-10"><a href="#cb1-10" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;MAJOR_VERSION&quot;</span><span class="fu">:</span> <span class="st">&quot;1.20.14&quot;</span><span class="fu">,</span></span>
<span id="cb1-11"><a href="#cb1-11" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;REVISION&quot;</span><span class="fu">:</span> <span class="st">&quot;132e719ef314b40f352e6399034d68a9a95e95ef&quot;</span></span>
<span id="cb1-12"><a href="#cb1-12" aria-hidden="true" tabindex="-1"></a>    <span class="fu">}</span></span>
<span id="cb1-13"><a href="#cb1-13" aria-hidden="true" tabindex="-1"></a><span class="fu">}</span></span></code></pre></div></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p><code>GET /_node/health?probes=#probe1,#probe2</code></p></td>
<td style="text-align: left;"><p>Gets the health status of the
component. Probes can be filtered using the optional <code>probes</code>
query param. The parameter can handle a list of probes, separated by
commas (<code>,</code>). If no query param, you get the health of all
probes. If the return status is 200 then everything is ok, if 500, there
is at least one error. This endpoint can be used by a load balancer, to
determine if a component instance is not in the pool, for example.</p>
<p>Some probes are not displayed by default. You have to explicitly use
the query param to retrieve them. These probes are:</p>
<p>- <strong>cpu</strong></p>
<p>- <strong>memory</strong></p>
<p>- <strong>api-sync</strong></p>
<p>Those probes are considered healthy if there are under a configurable
threshold (default is 80%). To configure it, add in your
<code>gravitee.yml</code>:</p>
<p>[source, yml] ---- services: health: threshold: cpu: 80 memory: 80
----</p></td>
<td
style="text-align: left;"><p><code>GET /_node/health?probes=management-api,management-repository</code></p>
<div class="sourceCode" id="cb2"><pre
class="sourceCode json"><code class="sourceCode json"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="er">HTTP/1.1</span> <span class="er">200</span> <span class="er">OK</span></span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a><span class="er">Content-Type:</span> <span class="er">application/json</span></span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a><span class="fu">{</span></span>
<span id="cb2-5"><a href="#cb2-5" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;management-api&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb2-6"><a href="#cb2-6" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;healthy&quot;</span><span class="fu">:</span> <span class="kw">true</span></span>
<span id="cb2-7"><a href="#cb2-7" aria-hidden="true" tabindex="-1"></a>    <span class="fu">},</span></span>
<span id="cb2-8"><a href="#cb2-8" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;management-repository&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb2-9"><a href="#cb2-9" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;healthy&quot;</span><span class="fu">:</span> <span class="kw">true</span></span>
<span id="cb2-10"><a href="#cb2-10" aria-hidden="true" tabindex="-1"></a>    <span class="fu">},</span></span>
<span id="cb2-11"><a href="#cb2-11" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;api-sync&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb2-12"><a href="#cb2-12" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;healthy&quot;</span><span class="fu">:</span> <span class="kw">true</span></span>
<span id="cb2-13"><a href="#cb2-13" aria-hidden="true" tabindex="-1"></a>    <span class="fu">},</span></span>
<span id="cb2-14"><a href="#cb2-14" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;api-sync&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb2-15"><a href="#cb2-15" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;healthy&quot;</span><span class="fu">:</span> <span class="kw">true</span></span>
<span id="cb2-16"><a href="#cb2-16" aria-hidden="true" tabindex="-1"></a>    <span class="fu">}</span></span>
<span id="cb2-17"><a href="#cb2-17" aria-hidden="true" tabindex="-1"></a><span class="fu">}</span></span></code></pre></div></td>
</tr>
<tr class="even">
<td
style="text-align: left;"><p><code>GET /_node/configuration</code></p></td>
<td style="text-align: left;"><p>Gets the node configuration from the
<code>gravitee.yml</code> file and/or environment variables.</p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb3"><pre
class="sourceCode json"><code class="sourceCode json"><span id="cb3-1"><a href="#cb3-1" aria-hidden="true" tabindex="-1"></a><span class="er">HTTP/1.1</span> <span class="er">200</span> <span class="er">OK</span></span>
<span id="cb3-2"><a href="#cb3-2" aria-hidden="true" tabindex="-1"></a><span class="er">Content-Type:</span> <span class="er">application/json</span></span>
<span id="cb3-3"><a href="#cb3-3" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb3-4"><a href="#cb3-4" aria-hidden="true" tabindex="-1"></a><span class="fu">{</span></span>
<span id="cb3-5"><a href="#cb3-5" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;analytics.elasticsearch.endpoints[0]&quot;</span><span class="fu">:</span> <span class="st">&quot;http://${ds.elastic.host}:${ds.elastic.port}&quot;</span><span class="fu">,</span></span>
<span id="cb3-6"><a href="#cb3-6" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;analytics.type&quot;</span><span class="fu">:</span> <span class="st">&quot;elasticsearch&quot;</span><span class="fu">,</span></span>
<span id="cb3-7"><a href="#cb3-7" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;ds.elastic.host&quot;</span><span class="fu">:</span> <span class="st">&quot;localhost&quot;</span><span class="fu">,</span></span>
<span id="cb3-8"><a href="#cb3-8" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;ds.elastic.port&quot;</span><span class="fu">:</span> <span class="dv">9200</span><span class="fu">,</span></span>
<span id="cb3-9"><a href="#cb3-9" aria-hidden="true" tabindex="-1"></a>    <span class="er">...</span></span>
<span id="cb3-10"><a href="#cb3-10" aria-hidden="true" tabindex="-1"></a><span class="fu">}</span></span></code></pre></div></td>
</tr>
<tr class="odd">
<td
style="text-align: left;"><p><code>GET /_node/monitor</code></p></td>
<td style="text-align: left;"><p>Gets monitoring information from the
JVM and the server.</p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb4"><pre
class="sourceCode json"><code class="sourceCode json"><span id="cb4-1"><a href="#cb4-1" aria-hidden="true" tabindex="-1"></a><span class="er">HTTP/1.1</span> <span class="er">200</span> <span class="er">OK</span></span>
<span id="cb4-2"><a href="#cb4-2" aria-hidden="true" tabindex="-1"></a><span class="er">Content-Type:</span> <span class="er">application/json</span></span>
<span id="cb4-3"><a href="#cb4-3" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb4-4"><a href="#cb4-4" aria-hidden="true" tabindex="-1"></a><span class="fu">{</span></span>
<span id="cb4-5"><a href="#cb4-5" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;jvm&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb4-6"><a href="#cb4-6" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;gc&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb4-7"><a href="#cb4-7" aria-hidden="true" tabindex="-1"></a>            <span class="dt">&quot;collectors&quot;</span><span class="fu">:</span> <span class="ot">[</span></span>
<span id="cb4-8"><a href="#cb4-8" aria-hidden="true" tabindex="-1"></a>                <span class="fu">{</span></span>
<span id="cb4-9"><a href="#cb4-9" aria-hidden="true" tabindex="-1"></a>                    <span class="dt">&quot;collectionCount&quot;</span><span class="fu">:</span> <span class="dv">7</span><span class="fu">,</span></span>
<span id="cb4-10"><a href="#cb4-10" aria-hidden="true" tabindex="-1"></a>                    <span class="dt">&quot;collectionTime&quot;</span><span class="fu">:</span> <span class="dv">98</span><span class="fu">,</span></span>
<span id="cb4-11"><a href="#cb4-11" aria-hidden="true" tabindex="-1"></a>                    <span class="dt">&quot;name&quot;</span><span class="fu">:</span> <span class="st">&quot;young&quot;</span></span>
<span id="cb4-12"><a href="#cb4-12" aria-hidden="true" tabindex="-1"></a>                <span class="fu">}</span><span class="ot">,</span></span>
<span id="cb4-13"><a href="#cb4-13" aria-hidden="true" tabindex="-1"></a>                <span class="fu">{</span></span>
<span id="cb4-14"><a href="#cb4-14" aria-hidden="true" tabindex="-1"></a>                    <span class="dt">&quot;collectionCount&quot;</span><span class="fu">:</span> <span class="dv">3</span><span class="fu">,</span></span>
<span id="cb4-15"><a href="#cb4-15" aria-hidden="true" tabindex="-1"></a>                    <span class="dt">&quot;collectionTime&quot;</span><span class="fu">:</span> <span class="dv">189</span><span class="fu">,</span></span>
<span id="cb4-16"><a href="#cb4-16" aria-hidden="true" tabindex="-1"></a>                    <span class="dt">&quot;name&quot;</span><span class="fu">:</span> <span class="st">&quot;old&quot;</span></span>
<span id="cb4-17"><a href="#cb4-17" aria-hidden="true" tabindex="-1"></a>                <span class="fu">}</span></span>
<span id="cb4-18"><a href="#cb4-18" aria-hidden="true" tabindex="-1"></a>            <span class="ot">]</span></span>
<span id="cb4-19"><a href="#cb4-19" aria-hidden="true" tabindex="-1"></a>        <span class="fu">},</span></span>
<span id="cb4-20"><a href="#cb4-20" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;mem&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb4-21"><a href="#cb4-21" aria-hidden="true" tabindex="-1"></a>    <span class="er">...</span></span>
<span id="cb4-22"><a href="#cb4-22" aria-hidden="true" tabindex="-1"></a><span class="fu">}</span></span></code></pre></div></td>
</tr>
</tbody>
</table>
