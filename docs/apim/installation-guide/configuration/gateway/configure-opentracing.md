# Why Should I Enable OpenTracing?

Using OpenTracing allows Gravitee to trace every request that comes
through the APIM Gateway, creating a deep level of insight on API
policies and making debugging a cinch. Without OpenTracing, you’ll only
receive limited details – making monitoring and troubleshooting
complicated and time-consuming.

So, if you’re looking for a way to simplify debugging, improve
monitoring, and enhance visibility into requests across multiple
services, Gravitee’s OpenTracing solution with Jaeger as a tracer has
you covered. Learn how to set up OpenTracing with the instructions
below.

# How To Enable OpenTracing

In the `gravitee.yml` file, enable tracing by adding the following
configuration:

    tracing:
        enabled: true
        type: jaeger
        jaeger:
        host: localhost
        port: 14250

Here, you **must** change `enabled` from `false` to `true`.

And that’s it! You’ve enabled OpenTracing on APIM Gateway.

Want to try it yourself in Docker? link:{{
*/apim/3.x/apim\_opentracing\_in\_docker.html* | relative\_url }}\[Click
here\] for more details.
