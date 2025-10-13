# Custom Policies

## Overview

Policies are rules or logic that can be executed by the API Gateway. A policy acts as a proxy controller by guaranteeing that a given business rule is fulfilled during the processing of an API transaction. This article describes how to build and deploy your own policies.

## Policy skeleton generation

{% hint style="warning" %}
Ensure [OSS repositories](http://central.sonatype.org/pages/ossrh-guide.html) are activated in your [Maven settings](https://maven.apache.org/settings.html)
{% endhint %}

To demonstrate how to develop a policy, the following example creates the FooHeaderCheck policy to validate if requests contain the `X-Foo` header.&#x20;

{% hint style="info" %}
The `gravitee-policy-maven-archetype` automatically adds "Policy" to the policy name you specify
{% endhint %}

The skeleton for this policy can be generated with the following code:

```bash
mvn archetype:generate\
    -DarchetypeGroupId=io.gravitee.maven.archetypes\
    -DarchetypeArtifactId=gravitee-policy-maven-archetype\
    -DarchetypeVersion=1.10.1\
    -DartifactId=foo-header-check-policy\
    -DgroupId=my.gravitee.extension.policy\
    -Dversion=1.0.0-SNAPSHOT\
    -DpolicyName=FooHeaderCheck
```

This generates the `foo-header-check-policy` directory with the following structure:

```bash
.
├── pom.xml
├── README.md
└── src
    ├── assembly
    │   └── policy-assembly.xml
    ├── main
    │   ├── java
    │   │   └── my
    │   │       └── gravitee
    │   │           └── extension
    │   │               └── policy
    │   │                   ├── FooHeaderCheckPolicyConfiguration.java
    │   │                   └── FooHeaderCheckPolicy.java
    │   └── resources
    │       └── plugin.properties
    └── test
        └── java
            └── my
                └── gravitee
                    └── extension
                        └── policy
                            └── FooHeaderCheckPolicyTest.java
```

The following files are generated:

| File                                     | Description                                                               |
| ---------------------------------------- | ------------------------------------------------------------------------- |
| `pom.xml`                                | The main Maven POM file                                                   |
| `README.md`                              | The main entry point for the policy documentation                         |
| `policy-assembly.xml`                    | The common Maven assembly descriptor for any policies                     |
| `FooHeaderCheckPolicyConfiguration.java` | The policy configuration class                                            |
| `plugin.properties`                      | The policy descriptor file                                                |
| `FooHeaderCheckPolicyTest.java`          | The [JUnit](http://junit.org/) unit test class for this policy            |
| `FooHeaderCheckPolicy.java`              | The main policy class that contains business code to implement the policy |

{% tabs %}
{% tab title="pom.xml" %}
Gravitee projects are [Maven](https://maven.apache.org/)-managed. A policy project is described via the Maven [Project Object Model](https://maven.apache.org/pom.html) file.
{% endtab %}

{% tab title="README.md" %}
Each policy should by documented by a dedicated `README.md` file that contains comprehensive information related to the use of your policy.
{% endtab %}

{% tab title="undefined" %}
A policy is a type of Gravitee plugin. It can be integrated into the APIM Gateway using the distribution file built from `policy-assembly.xml`. Below is the distribution file structure for the example FooCheckHeader policy:

```bash
.
├── foo-header-check-policy-1.0.0-SNAPSHOT.jar
├── lib
└── schemas
    └── urn:jsonschema:my:gravitee:extension:policy:FooHeaderCheckPolicyConfiguration.json
```

The following files/folders are generated:

<table><thead><tr><th width="293">File</th><th>Description</th></tr></thead><tbody><tr><td><code>foo-header-check-policy-1.0.0-SNAPSHOT.jar</code></td><td>The main policy Jar file</td></tr><tr><td><code>lib/</code></td><td>Where the external dependencies are stored (from the <a href="https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html">Maven POM file dependencies</a>)</td></tr><tr><td><code>schemas/</code></td><td>Where the JSON configuration schemas are stored</td></tr></tbody></table>
{% endtab %}

{% tab title="FooHeaderCheckPolicyConfiguration.java" %}
This is the policy configuration. It is described by one or several [Java Bean](http://docs.oracle.com/javase/tutorial/javabeans/) class(es) where each attribute is a configuration parameter. During packaging, the configuration is compiled into JSON schemas using Gravitee's [json-schema-generator-maven-plugin](https://github.com/gravitee-io/json-schema-generator-maven-plugin). These are read by the Gateway and used to parse [API definitions](https://github.com/gravitee-io/gravitee-gateway). Policy configuration is injected into the policy class instance at runtime and can be used during implementation.
{% endtab %}

{% tab title="plugin.properties" %}
Each policy plugin is described by the `plugin.properties` descriptor, which declares the following parameters:

<table><thead><tr><th width="162.99999999999997">Parameter</th><th width="257">Description</th><th>Default value</th></tr></thead><tbody><tr><td><code>id</code></td><td>The policy identifier</td><td>policy artifact id</td></tr><tr><td><code>name</code></td><td>The policy name</td><td>N/A (mandatory parameter)</td></tr><tr><td><code>version</code></td><td>The policy version</td><td>N/A (mandatory parameter)</td></tr><tr><td><code>description</code></td><td>The policy description</td><td>"Description of the <em>Policy name</em> Gravitee Policy"</td></tr><tr><td><code>class</code></td><td>The main policy class</td><td>Path to the generated class file</td></tr><tr><td><code>type</code></td><td>The type of Gravitee plugin</td><td><code>policy</code></td></tr><tr><td><code>category</code></td><td>The policy category</td><td></td></tr><tr><td><code>icon</code></td><td>The policy icon</td><td></td></tr><tr><td><code>proxy</code></td><td>The policy's proxy manifest data</td><td>N/A (options include REQUEST, RESPONSE)</td></tr><tr><td><code>message</code></td><td>The policy's message manifest data</td><td>N/A (options include REQUEST, RESPONSE, MESSAGE_REQUEST, MESSAGE_RESPONSE)</td></tr></tbody></table>

{% hint style="info" %}
**Policy ID**

A policy is enabled when declared in the API definition. Ensure the policy identifier is defined correctly. It may be hard to rename if many API definitions link to it.
{% endhint %}
{% endtab %}
{% endtabs %}

## Policy Application

A policy can be applied to the Request phase of the proxy chain, the Response phase, or both.

{% tabs %}
{% tab title="Apply to Request" %}
A policy can be applied to the proxy Request phase by implementing a method that handles the `io.gravitee.gateway.api.policy.annotations.OnRequest` annotation. For example:

```java
@OnRequest
public void onRequest(Request request, Response response, PolicyChain policyChain) {
    // Add a dummy header
    request.headers().set("X-DummyHeader", configuration.getDummyHeaderValue());

    // Finally continue chaining
    policyChain.doNext(request, response);
}
```

{% hint style="info" %}
The `PolicyChain` must always be called with `PolicyChain#doNext()` or `PolicyChain#failWith()` to properly terminate `onRequest` processing&#x20;
{% endhint %}
{% endtab %}

{% tab title="Apply to Response" %}
A policy can be applied to the proxy Response phase by implementing a method that handles the `io.gravitee.gateway.api.policy.annotations.OnResponse` annotation. For example:

```java
@OnResponse
public void onResponse(Request request, Response response, PolicyChain policyChain) {
    if (isASuccessfulResponse(response)) {
        policyChain.doNext(request, response);
    } else {
        policyChain.failWith(new PolicyResult() {
            @Override
            public boolean isFailure() {
                return true;
            }

            @Override
            public int httpStatusCode() {
                return HttpStatusCode.INTERNAL_SERVER_ERROR_500;
            }

            @Override
            public String message() {
                return "Not a successful response :-(";
            }
        });
    }
}

private static boolean isASuccessfulResponse(Response response) {
    switch (response.status() / 100) {
        case 1:
        case 2:
        case 3:
            return true;
        default:
            return false;
    }
}
```

{% hint style="info" %}
The `PolicyChain` must always be called with `PolicyChain#doNext()` or `PolicyChain#failWith()` to properly terminate `onResponse` processing&#x20;
{% endhint %}
{% endtab %}

{% tab title="Apply to both" %}
A policy is not restricted to only one Gateway proxy phase. It can be applied during both the Request and Response phases by using both annotations in the same class.
{% endtab %}
{% endtabs %}

### Provided parameters

Annotated methods can declare parameters which are automatically provided by the Gateway at runtime. Available parameters are:

<table><thead><tr><th width="288">Parameter class</th><th width="117">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td><code>io.gravitee.gateway.api.Request</code></td><td>No</td><td>Wrapper to the Request object containing all information about the processed request (URI, parameters, headers, input stream, …)</td></tr><tr><td><code>io.gravitee.gateway.api.Response</code></td><td>No</td><td>Wrapper to the Response object containing all information about the processed response (status, headers, output stream, …)</td></tr><tr><td><code>io.gravitee.gateway.api.policy.PolicyChain</code></td><td>Yes</td><td>The current policy chain that gives control to the policy to continue (<code>doNext</code>) or reject (<code>failWith</code>) the chain</td></tr><tr><td><code>io.gravitee.gateway.api.policy.PolicyContext</code></td><td>No</td><td>The policy context that can be used to get contextualized objects (API store, …)</td></tr></tbody></table>
