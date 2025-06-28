# GraphQL Rate Limit

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../../../4.6/overview/gravitee-apim-enterprise-edition/)**.**
{% endhint %}

## Overview

The GraphQL Rate Limit policy provides basic rate limiting for GraphQL queries.

Unlike a traditional rate-limiting policy, where a weight of 1 is applied to every incoming request, the `graphql-rate-limit` policy calculates the cost of the GraphQL query and considers this cost to be the weight.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 TCP proxy APIs or v4 message APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
```graphql
query { # + 1
  allPeople(first:20) { # * 20 + 1
    people { # + 1
      name # + 1
      vehicleConnection(first:10) { # * 10 + 1
        vehicles { # + 1
          id  # + 1
          name # + 1
          cargoCapacity # + 1
        }
      }
    }
  }
}
```

The total cost for the above GraphQL query is: ((((4 \* 10 + 1) + 1) + 1) \* 20 + 1) + 1 = 862
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `graphql-rate-limit` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="208.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `graphql-rate-limit` policy can be configured with the following options:

### Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

<table><thead><tr><th width="165">Property</th><th width="100" data-type="checkbox">Required</th><th width="207">Description</th><th width="94">Type</th><th>Default</th></tr></thead><tbody><tr><td>limit</td><td>true</td><td>Static limit on the number of GraphQL queries that can be sent.</td><td>integer</td><td>0</td></tr><tr><td>periodTime</td><td>true</td><td>Time duration</td><td>Integer</td><td>1</td></tr><tr><td>periodTimeUnit</td><td>true</td><td>Time unit ("SECONDS", "MINUTES" )</td><td>String</td><td>SECONDS</td></tr><tr><td>maxCost</td><td>false</td><td>A defined maximum cost per query. 0 means unlimited.</td><td>integer</td><td>0</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `graphql-rate-limit` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th></tr></thead><tbody><tr><td>1.0+</td><td>4.3+</td></tr></tbody></table>

## Errors

<table><thead><tr><th width="108">Phase</th><th width="73">Code</th><th width="227">Error template key</th><th>Description</th></tr></thead><tbody><tr><td>*</td><td><code>400</code></td><td>GRAPHQL_RATE_LIMIT_REACH_MAX_COST</td><td>When the query reaches the max cost</td></tr><tr><td>*</td><td><code>429</code></td><td>GRAPHQL_RATE_LIMIT_TOO_MANY_REQUESTS</td><td>When too many requests have been made according to the rate limiting configuration</td></tr></tbody></table>
