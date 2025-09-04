---
noIndex: true
---

# Package and share my intercepts

## Introduction

While telepresence takes cares of the interception part of your setup, you usually still need to script some boiler plate code to run the local part (the handler) of your code.

Classic solutions rely on a Makefile, or bash scripts, but this becomes cumbersome to maintain.

Instead, you can use [telepresence intercept specs](../technical-reference/intercepts/configure-intercept-using-specifications.md): They allow you to specify all aspects of an intercept, including prerequisites, the local processes that receive the intercepted traffic, and the actual intercept. Telepresence can then run the specification.

## Getting started

You will need a Kubernetes cluster, a deployment, and a service to begin using an Intercept Specification.

Once you have a Kubernetes cluster you can apply this configuration to start an echo easy deployment that we can then use for our Intercept Specification

You can create the local yaml file by using

```console
$ cat > echo-server.yaml <<EOF
---
apiVersion: v1
kind: Service
metadata:
  name: "echo-easy"
spec:
  type: ClusterIP
  selector:
    service: echo-easy
  ports:
    - name: proxied
      port: 80
      targetPort: http
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: "echo-easy"
  labels:
    service: echo-easy
spec:
  replicas: 1
  selector:
    matchLabels:
      service: echo-easy
  template:
    metadata:
      labels:
        service: echo-easy
    spec:
      containers:
        - name: echo-easy
          image: jmalloc/echo-server
          ports:
            - containerPort: 8080
              name: http
          resources:
            limits:
              cpu: 50m
              memory: 128Mi
```

And then apply it using

```bash
kubectl apply -f echo-server.yaml
```

## Spinning up a local environment with one command

First, you must create an intercept spec. The following is an example spec. It will run `echo hello` before starting the intercept, then will launch `thhal/echo-server:latest` as an handler for a workload (i.e. deployment or statefulset) named `echo`, at port `8080`, and finally it will run `echo goodbye`:

All you have to do is locally create this spec:

```console
$ cat > my-intercept.yaml <<EOF
prerequisites:
  - create: hello
    delete: goodbye
workloads:
  - name: echo-easy
    intercepts:
      - handler: echo-easy
        headers:
          - name: who
            value: {{ env "USER" }}
        previewURL:
          enable: true
connection:
  context: default
handlers:
  - name: echo-easy
    docker:
      image: jmalloc/echo-server:latest
  - name: hello
    script:
      run: echo hello
  - name: goodbye
    script:
      run: echo goodbye
```

And then you can launch it:

```bash
telepresence intercept run my-intercept.yaml
```
