# Monitoring GKO

## Overview

In this section, you will learn how to set up and deploy monitoring capabilities for a Gravitee Kubernetes Operator (GKO) on an existing Gravitee API Management (APIM) ready Kubernetes cluster.

{% hint style="info" %}
If you do not have an existing Gravitee Kubernetes Operator deployment, see the [GKO Deployment Guide](../../getting-started/install-guides/install-on-kubernetes/install-gravitee-kubernetes-operator.md) first.
{% endhint %}

## Prerequisites

Before you start the monitoring deployment process, ensure that you have access to the following libraries:

* The kubectl command-line tool installed on your local machine and configured to connect to your cluster. Learn more about installing kubectl in the [official Kubernetes documentation](https://kubernetes.io/docs/tasks/tools/).
* The Helm package manager installed on your local machine. Learn more about installing Helm in the [official Helm documentation](https://helm.sh/docs/intro/install/).

## Deploying the Prometheus Stack

The [kube-prometheus repository](https://github.com/prometheus-operator/kube-prometheus) is a collection of Kubernetes manifests, [Grafana](https://grafana.com/) dashboards, and [Prometheus rules](https://prometheus.io/), combined with documentation and scripts to provide easy-to-operate, end-to-end Kubernetes cluster monitoring with Prometheus using the Prometheus Operator.

### Run the deployment script

Run the following commands in your command-line tool (the working directory is irrelevant) to create the namespace to be used to deploy the Prometheus stack:

```sh
$ kubectl create namespace monitoring
$ kubectl config set-context --current --namespace=monitoring
```

Then run the following commands to deploy the Prometheus stack:

{% code overflow="wrap" %}
```sh
$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
$ helm repo update
$ helm install prometheus prometheus-community/kube-prometheus-stack --debug
```
{% endcode %}

Check if Prometheus and Grafana have been installed correctly:

```sh
kubectl get svc -n monitoring
```

The command-line output should include `prometheus-grafana` and `prometheus-kube-prometheus-prometheus`, as shown in the example below:

```
NAME                                      TYPE        EXTERNAL-IP   PORT(S)                      AGE
prometheus-kube-state-metrics             ClusterIP   <none>        8080/TCP                     3m9s
prometheus-prometheus-node-exporter       ClusterIP   <none>        9100/TCP                     3m9s
prometheus-grafana                        ClusterIP   <none>        80/TCP                       3m9s
prometheus-kube-prometheus-prometheus     ClusterIP   <none>        9090/TCP                     3m9s
prometheus-kube-prometheus-operator       ClusterIP   <none>        443/TCP                      3m9s
prometheus-kube-prometheus-alertmanager   ClusterIP   <none>        9093/TCP                     3m9s
alertmanager-operated                     ClusterIP   <none>        9093/TCP,9094/TCP,9094/UDP   2m52s
prometheus-operated                       ClusterIP   <none>        9090/TCP                     2m51s
```

To access the Grafana dashboard, run the following command:

```sh
kubectl port-forward -n monitoring svc/prometheus-grafana 8000:80
```

Grafana is now available at [http://localhost:8000](http://localhost:8000/). An admin user is created by default. To find out the password for that user, run the following command:

{% code overflow="wrap" %}
```sh
kubectl get secrets prometheus-grafana -n monitoring -o jsonpath='{.data.admin-password}'|base64 -d
```
{% endcode %}

### Link the Prometheus stack to the GKO

The Prometheus resource declaratively describes the desired state of a Prometheus deployment, while `ServiceMonitor` resources describe the targets to be monitored by Prometheus. The GKO provides a basic `ServiceMonitor` resource that can be discovered by Prometheus. To enable this, run the following command:

{% code overflow="wrap" %}
```sh
kubectl apply -f https://raw.githubusercontent.com/gravitee-io/gravitee-kubernetes-operator/alpha/config/prometheus/monitor.yaml
```
{% endcode %}

To check if the `ServiceMonitor` resource has been created, run the following command:

```sh
kubectl get servicemonitors -n gko-system
```

The command-line output should include `controller-manager-metrics-monitor`, as shown in the example below:

```
NAME                                 AGE
controller-manager-metrics-monitor   21s
```

{% hint style="warning" %}
Most of the actions described above are not persistent and should mainly be used for development/test purposes and not in production.
{% endhint %}
