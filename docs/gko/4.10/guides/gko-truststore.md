# Configure GKO TrustStore

If you have self-signed certificates, you can easily configure GKO to use your CA certificate and connect to APIM securely. First of all make sure that you already created a secret using you CA pem in your cluster

```sh
kubectl create secret generic my-ca-secret --from-file=cert.pem=ca.pem
```

You have 2 options to add this secret to GKO
### 1. Adding the secret to the default location `/etc/ssl/certs`
If you want to add your CA cert to the default location, all you need is to add the following lines to your values.yaml

```yaml
manager:
  volumes:
    - name: ca-pem-volume
      secret:
        secretName: my-ca-secret
  volumeMounts:
    - name: ca-pem-volume
      mountPath: /etc/ssl/certs
      readOnly: true
```

### 2. Adding the secret to your custom location
To add your CA cert to its dedicated location, you can set "manager.httpClient.trustStore.path". Adding the following lines to your values.yaml will let GKO to pick up your CA cert from its dedicated location.

```yaml
manager:
  httpClient:
    trustStore:
      path: "/etc/ca/cert.pem"
  volumes:
    - name: ca-pem-volume
      secret:
        secretName: my-ca-secret
  volumeMounts:
    - name: ca-pem-volume
      mountPath: /etc/ca/
      readOnly: true
```
