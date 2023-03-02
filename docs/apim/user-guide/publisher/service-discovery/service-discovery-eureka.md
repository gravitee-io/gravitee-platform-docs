# service-discovery-eureka

:page-sidebar: apim\_3\_x\_sidebar :page-permalink: apim/3.x/apim\_service\_discovery\_eureka.html :page-folder: apim/user-guide/publisher/service-discovery :page-layout: apim3x :page-title: Eureka service discovery

\== Configuration

The configuration is loaded from the common GraviteeIO Gateway configuration file (gravitee.yml) All configurations described by official Eureka discovery client documentation are available on the official github repository: https://github.com/Netflix/eureka/wiki. Gravitee Gateway uses Eureka Discovery client v1 and fetch configured Eureka Servers. It does not register the gateway application into Eureka registry. Please refer the official Eureka documentation for advanced uses and advanced concepts.

For more information, see the complete link:\{{ 'https://github.com/gravitee-io-community/gravitee-service-discovery-eureka/blob/master/README.adoc' \}}\[Eureka client configuration].

\== Enable Eureka Service Discovery in Gravitee APIM

Once you have configured your Eureka service, go to the APIM console:

. Create or select an existing API. . Under API's submenu, click _Proxy_. . Under _Backend Service_, select _Endpoints_.

image::

\[]

\[start=4] . Click on the _Edit Group_ icon. . Select the _SERVICE DISCOVERY_ tab. . Click the _Enabled service discovery_ checkbox to activate this option. . Select _Eureka Service Discovery_ in the _Type_ dropdown list. . For _Application_, enter your application name.

image::

\[]

\[start=9] . Click _SAVE_.

Your API should now appear out of sync in the top banner - click _deploy your API_ to rectify this

image::

\[]

NOTE: Gravitee Gateway will not remove endpoints configured through the APIM console before service discovery was enabled - it will continue to consider such endpoints in addition to the ones dynamically discovered through Eureka integration (these are not shown in the APIM console). You can manually remove any endpoints defined through the APIM console. However, it is highly recommended that you keep at least one such endpoint declared as secondary - secondary endpoints are not included in the load-balancer pool and are only selected to handle requests if Eureka is no longer responding.

To declare an endpoint as secondary:

. Click on the _Edit_ icon. . Click the _Secondary endpoint_ checkbox to enable it. . Select _SAVE_.

image::

\[]

\== Verify that your service is properly discovered by the APIM gateway

To verify that your service has been successfully discovered through Eureka, check out the API gateway logs:

### \[source]

### INFO i.g.g.h.a.m.impl.ApiManagerImpl - API id\[194c560a-fcd1-4e26-8c56-0afcd17e2630] name\[Time] version\[1.0.0] has been updated INFO i.g.g.s.e.d.v.EndpointDiscoveryVerticle - Receiving a service discovery event id\[eureka:whattimeisit] type\[REGISTER]

You can now try to call your API to make sure that incoming API requests are properly routed to the right backend service.

### \[source,bash]

### curl -X PUT -v "http://localhost:8082/whattimeisit"

If you encounter any issues, enable logs in order to troubleshoot. Refer to the link:\{{'/apim/3.x/apim\_publisherguide\_logging\_analytics.html#logs' | relative\_url\}}\[Logging and analytics documentation] to learn how to configure logging on your API.

\== Additional considerations

\=== Enable Health Check to monitor backend endpoints managed by Eureka

To view the status of all endpoints, including the ones managed by Eureka, enable the Health Check option for your API in the _Per-endpoint availability_ section.

image::

\[]

See the link:\{{'/apim/3.x/apim\_publisherguide\_backend\_services.html#configure\_health\_check' | relative\_url\}}\[Health Check documentation] for more information on how to enable the Health Check option for your API.
