# Installing The Kafka Gateway With Docker And Kubernetes

Gravitee's kafka Gateway can be deployed using Docker compose for local tests, or on Kubernetes for more realistic scenarios. this page shows a mix of both, but some steps may be missing.

## What You Will Learn
- how to start kafka gateway with docker
- how to move the same config to kubernetes
- some basic troubleshooting tips

## Requirements
* jdk 11
* docker / docker desktop
* kubectl
* a kubeconfig pointing at some cluster
* (optionnal) helm

### Quickstart docker compose
1. clone gravitee-io/kafka-gateway repo
2. run `docker compose up` in the examples/docker-compose folder
3. when logs show "started gateway" you are ready

### move to Kubernetes
#### apply manifests
run:

``` 
# WARNING: this is not exact yaml, just an example
kubectl apply -f k8s/
```

##### check pods
Use:
```bash
kubectl get pods -n gravitee-kafka-gw
```

If pods are CrashLoopBackOff, maybe the configuration is wrong or the kafka broker is not reachable or some other issue.

### TROUBLESHOOT
if something fails:
- look at pod logs
- maybe restart the namespace
- check that the docker compose example is still running?

## Next Steps
Read the APIM docs to learn how to connect api gateways to the kafka gateway.
