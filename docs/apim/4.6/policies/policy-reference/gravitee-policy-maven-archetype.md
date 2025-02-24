= gravitee-policy-maven-archetype

ifdef::env-github[]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-maven-archetype/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-maven-archetype/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-maven-archetype.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-maven-archetype"]
image:https://f.hubspotusercontent40.net/hubfs/7600448/gravitee-github-button.jpg["Join the community forum", link="https://community.gravitee.io?utm_source=readme", height=20]
endif::[]

Maven Archetype to create a Gravitee Policy

== Get started

A Policy is a step in the Request/Response Gateway proxy chain. A Policy acts as a *proxy controller* by guaranteeing if a given business rule is fulfilled during the Request/Response processing.

Archetype is already registered into the http://central.sonatype.org/pages/ossrh-guide.html[OSS repositories]. Don't forget to activate them in your Maven settings.

== Policy generation

Suppose you want to create a Policy that control if request contains the ``X-Foo`` header. Let's name it the *Foo header check policy*. Then you could generate your Policy like this:

```bash
mvn archetype:generate\
 -DarchetypeGroupId=io.gravitee.maven.archetypes\
 -DarchetypeArtifactId=gravitee-policy-maven-archetype\
 -DarchetypeVersion=1.10.0\
 -DartifactId=foo-header-check-policy\
 -DgroupId=my.gravitee.extension.policy\
 -Dversion=1.0.0-SNAPSHOT\
 -DpolicyName=FooHeaderCheck\
 -DtestingGatewayVersion=3.18.0
```

Once executed and parameters confirmed, the above command will create the ``foo-header-check-policy`` directory containing the following structure:

```
.
├── pom.xml
├── README.adoc
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

Hereafter a description about the different generated files:

|===
| File    | Description

| pom.xml | The main Maven POM file
| README.adoc | The main entry point for documentation of the Policy
| policy-assembly.xml | The common Maven assembly descriptor for any Policies
| FooHeaderCheckPolicyConfiguration.java | The Policy configuration class
| FooHeaderCheckPolicy.java | The Policy class, from which the business behavior is implemented
| plugin.properties | The Policy descriptor file
| FooHeaderCheckPolicyTest.java | The Policy unit test Java class
|===

=== pom.xml

Each Policy (and more generally any Gravitee projects) is https://maven.apache.org/[Maven] managed. Thus, a Policy project is described by using the Maven https://maven.apache.org/pom.html[Project Object Model] file.

=== README.adoc

Each Policy should have a dedicated `README.adoc` file to document it. The `README.adoc` file should contain everything related to the use of your Policy: *What is its functionality? How can use it? How can configure it?*

=== policy-assembly.xml

A Policy is just a kind of Gravitee Plugin.

It can be plugged to the https://github.com/gravitee-io/gravitee-gateway[Gravitee Gateway] by using the distribution file built from the `policy-assembly.xml` file.

Based on our *FooHeaderCheck* Policy, the distribution file structure is the following:

```
.
├── foo-header-check-policy-1.0.0-SNAPSHOT.jar
├── lib
└── schemas
    └── urn:jsonschema:my:gravitee:extension:policy:FooHeaderCheckPolicyConfiguration.json
```

Hereafter a description about the different generated files:

|===
| File    | Description

| `foo-header-check-policy-1.0.0-SNAPSHOT.jar` | The main Policy jar file
| `lib/` | Where the external dependencies are stored (from the [Maven POM file dependencies](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)
| `schemas/` | Where the JSON configuration schemas are stored
|===

==== JSON Configuration schemas

Policy configuration is described inside one or several http://docs.oracle.com/javase/tutorial/javabeans/[Java Bean] classes (see the FooHeaderCheckPolicyConfiguration.java example).

During the packaging phase, each Policy configuration classes are processed to generate one or several http://json-schema.org/[JSON schema(s)] that will be read by the Gateway when the Policy will be plugged in.

JSON schema generation is done thanks to the Gravitee's https://github.com/gravitee-io/json-schema-generator-maven-plugin[json-schema-generator-maven-plugin] Maven plugin.

A JSON schema generated by the `json-schema-generator-maven-plugin` will only contain the base details of your policy configuration. You can find this generated file in the `target/schemas/` folder.

If you wish to include additional details, such as field names and descriptions, it is recommended to copy the generated JSON schema into a `src/main/schemas/schema-form.json` file and make your changes.

The example below shows some of the supported JSON schema fields:

``` json
{
  "type" : "object",
  "id" : "urn:jsonschema:my:gravitee:extension:policy:ExamplePolicyConfiguration",
  "properties" : {
    "stringParam" : {
      "title": "A Special String",
      "description": "This is a special string",
      "type" : "string"
    },
    "defaultValue" : {
      "title": "Default Value",
      "description": "Example of Default",
      "type" : "string",
      "default": "GET",
      "enum" : [ "CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE", "OTHER" ]
    }
  },
  "required": ["defaultValue"]
}
```

=== FooHeaderCheckPolicyConfiguration.java

The Policy configuration class.

Policy configuration is described into one or several http://docs.oracle.com/javase/tutorial/javabeans/[Java Bean] class(es) where each attribute is a configuration parameter.

During the package phase, Policy configuration is compiled into JSON Configuration schemas. These schemas are used to parse https://github.com/gravitee-io/gravitee-gateway[API definitions].

Policy configuration is finally injected to the Policy class instance at runtime and then can be used during implementation.

=== FooHeaderCheckPolicy.java

The main Policy class. Contains business code that implements the Policy.

A Policy can be applied on several parts of the proxy chain:

- The Request phase
- The Response phase
- Both of them

==== Apply Policy on the Request phase

A Policy can be applied to the proxy Request phase by just implementing a method dealing with the ``io.gravitee.gateway.api.policy.annotations.OnRequest`` annotation. For instance:

```java
@OnRequest
public void onRequest(Request request, Response response, PolicyChain policyChain) {
	// Add a dummy header
    request.headers().set("X-DummyHeader", configuration.getDummyHeaderValue());

	// Finally continue chaining
	policyChain.doNext(request, response);
}
```

> The `PolicyChain` **must always be called to end an *on Request* processing**. Be ware to make a call to the `PolicyChain=doNext()` or  `PolicyChain=failWith()`   to correctly end the *on Request* processing.

==== Apply Policy on the Response phase

A Policy can be applied to the proxy Response phase by just implementing a method dealing with the ``io.gravitee.gateway.api.policy.annotations.OnResponse`` annotation. For instance:

```java
@OnResponse
public void onResponse(Request request, Response response, PolicyChain policyChain) {
    if (isASuccessfulResponse(response)) {
        policyChain.doNext(request, response);
    } else {
        policyChain.failWith(
            PolicyResult.failure(HttpStatusCode.INTERNAL_SERVER_ERROR_500, "Not a successful response :-("));
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

> The `PolicyChain` **must always be called to end an *on Response* processing**. Be ware to make a call to the `PolicyChain=doNext()` or  `PolicyChain=failWith()`   to correctly end the *on Response* processing.

==== Apply Policy on both of Request and Response phases

A Policy is not restricted to only one Gateway proxy phase. It can be applied on both of the Request and Response phases by just using the both annotations in the same class.

==== Provided parameters

The annotated methods can declare several parameters (but not necessary all of them) which will be automatically provided by the Gateway at runtime.
Available provided parameters are:

|===
| Parameter class   | Mandatory | Description

| `io.gravitee.gateway.api.Request` | No | Wrapper to the Request object containing all information about the processed request (URI, parameters, headers, input stream, ...)
| `io.gravitee.gateway.api.Response` | No | Wrapper to the Response object containing all information about the processed response (status, headers, output stream, ...)
| `io.gravitee.gateway.api.policy.PolicyChain` | Yes | The current Policy chain that gives control to the Policy to continue (`doNext`) or reject (`failWith`) the current chain.
| `io.gravitee.gateway.api.policy.PolicyContext` | No | The Policy context that can be used to get contextualized objects (API store, ...).
|===

=== plugin.properties

As said, a Policy is a kind of Gravitee Plugin.

Each Plugin is described by the *plugin.properties* descriptor which declare the following parameters:

|===
| Parameter   | Description | Default value

| `id` | The Policy identifier     | Policy artifact id
| `name` | The Policy name     | N/A (mandatory parameter)
| `version` | The Policy version     | N/A (mandatory parameter)
| `description` | The Policy description     | "Description of the *Policy name* Gravitee Policy"
| `class` | The main Policy class     | Path to the generated class file
| `type` | The type of Gravitee Plugin     | `policy`
| `category` | The category the generated plugin will appear under in Design Studio | `others`
| `icon` | Custom icon file name | N/A (optional parameter)
|===

> A Policy is enabled when declared into the API definition. To do so, the Policy identifier is used to, as its name indicate, identify the Policy. Thus, **be ware to correctly choose the Policy identifier** from the beginning. It could be hard to rename it later if there are many of API definitions linked to it.

==== Custom Icons
In order to add a custom icon to your plugin, as displayed in Design Studio, you should:

. Include an image file (svg preferred) in the top level of your plugin
. Update the `plugin.properties` file and set `icon=your_file.svg`

=== FooHeaderCheckPolicyTest.java

The http://junit.org/[JUnit] unit test class for this Policy.

== Tip

Choose a short but clearly name for your Policy, **without precise the Policy suffix**. The `gravitee-policy-maven-archetype` will add it automatically.

For example, **do not** fill the ``policyName`` of your Policy like this:

```
-DpolicyName=AmazingStuffPolicy
```

but like this:

```
-DpolicyName=AmazingStuff
```
