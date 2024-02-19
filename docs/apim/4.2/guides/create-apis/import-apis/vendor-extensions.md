# Vendor Extensions

## Overview

You can use a vendor extension to add more information about your API to an OpenAPI specification.&#x20;

## Configuration

To use a vendor extension, add the `x-graviteeio-definition` field at the root of the specification. The value of this field is an `object` that follows this [JSON Schema](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/master/gravitee-apim-rest-api/gravitee-apim-rest-api-service/src/main/resources/schema/xGraviteeIODefinition.json).

Consider that:

* Categories must contain either a key or an ID.
* Only existing categories are imported.
* Import will fail if `virtualHosts` are already in use by other APIs.
* If set, `virtualHosts` will override `contextPath`.
* Groups must contain group names. Only existing groups are imported.
* `metadata.format` is case-sensitive. Possible values are:
  * STRING
  * NUMERIC
  * BOOLEAN
  * DATE
  * MAIL
  * URL
* Picture only accepts Data-URI format. Please see the example below.

### Example

<pre class="language-yaml"><code class="lang-yaml"><strong>openapi: "3.0.0"
</strong>info:
  version: 1.2.3
  title: Gravitee Echo API
  license:
    name: MIT
servers:
  - url: https://demo.gravitee.io/gateway/echo
x-graviteeio-definition:
  categories:
    - supplier
    - product
  virtualHosts:
    - host: api.gravitee.io
      path: /echo
      overrideEntrypoint: true
  groups:
    - myGroupName
  labels:
    - echo
    - api
  metadata:
    - name: relatedLink
      value: http://external.link
      format: URL
  picture: data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
  properties:
    - key: customHttpHeader
      value: X-MYCOMPANY-ID
  tags:
    - DMZ
    - partner
    - internal
  visibility: PRIVATE
paths:
...
</code></pre>
