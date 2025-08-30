# Monitoring

Telepresence offers powerful monitoring capabilities to help you keep a close eye on your telepresence activities and traffic manager metrics.

## Prometheus Integration

One of the key features of Telepresence is its seamless integration with Prometheus, which allows you to access real-time metrics and gain insights into your system's performance. With Prometheus, you can monitor various aspects of your traffic manager, including the number of active intercepts and users. Additionally, you can track consumption-related information, such as the number of intercepts used by your developers and how long they stayed connected.

To enable Prometheus metrics for your traffic manager, follow these steps:

1.  **Configure Prometheus Port**

    First, you'll need to specify the Prometheus port by setting a new environment variable called `PROMETHEUS_PORT` for your traffic manager. You can do this by running the following command:

    ```shell
    telepresence helm upgrade --set-string prometheus.port=9090
    ```
2.  **Validate the Prometheus Exposure**

    After configuring the Prometheus port, you can validate its exposure by port-forwarding the port using Kubernetes:

    ```shell
    kubectl port-forward deploy/traffic-manager 9090:9090 -n ambassador
    ```
3.  **Access Prometheus Dashboard**

    Once the port-forwarding is set up, you can access the Prometheus dashboard by navigating to `http://localhost:9090` in your web browser:

    Here, you will find a wealth of built-in metrics, as well as custom metrics (see below) that we have added to enhance your tracking capabilities.

    | **Name**                    | **Type** | **Description**                                                               | **Labels**                               |
    | --------------------------- | -------- | ----------------------------------------------------------------------------- | ---------------------------------------- |
    | `agent_count`               | Gauge    | Number of connected traffic agents.                                           |                                          |
    | `client_count`              | Gauge    | Number of connected clients.                                                  |                                          |
    | `active_intercept_count`    | Gauge    | Number of active intercepts.                                                  |                                          |
    | `session_count`             | Gauge    | Number of sessions.                                                           |                                          |
    | `tunnel_count`              | Gauge    | Number of tunnels.                                                            |                                          |
    | `tunnel_ingress_bytes`      | Counter  | Number of bytes tunnelled from clients.                                       |                                          |
    | `tunnel_egress_bytes`       | Counter  | Number of bytes tunnelled to clients.                                         |                                          |
    | `active_http_request_count` | Gauge    | Number of currently served HTTP requests.                                     |                                          |
    | `active_grpc_request_count` | Gauge    | Number of currently served gRPC requests.                                     |                                          |
    | `connect_count`             | Counter  | The total number of connects by user.                                         | `client`, `install_id`                   |
    | `connect_active_status`     | Gauge    | Flag to indicate when a connect is active. 1 for active, 0 for not active.    | `client`, `install_id`                   |
    | `intercept_count`           | Counter  | The total number of intercepts by user.                                       | `client`, `install_id`, `intercept_type` |
    | `intercept_active_status`   | Gauge    | Flag to indicate when an intercept is active. 1 for active, 0 for not active. | `client`, `install_id`, `workload`       |
4.  **Enable Scraping for Traffic Manager Metrics** To ensure that these metrics are collected regularly by your Prometheus server and to maintain a historical record, it's essential to enable scraping. If you're using the default Prometheus configuration, you can achieve this by specifying specific pod annotations as follows:

    ```yaml
    template:
      metadata:
        annotations:
          prometheus.io/path: /
          prometheus.io/port: "9090"
          prometheus.io/scrape: "true"
    ```

    These annotations instruct Prometheus to scrape metrics from the Traffic Manager pod, allowing you to track consumption metrics and other important data over time.

## Grafana Integration

Grafana plays a crucial role in enhancing Telepresence's monitoring capabilities. While the step-by-step instructions for Grafana integration are not included in this documentation, you have the option to explore the integration process. By doing so, you can create visually appealing and interactive dashboards that provide deeper insights into your telepresence activities and traffic manager metrics.

Moreover, we've developed a dedicated Grafana dashboard for your convenience. Below, you can find sample screenshots of the dashboard, and you can access the JSON model for configuration:

**Sample Screenshots:**

<figure><img src="../.gitbook/assets/00 tp 33.png" alt=""><figcaption></figcaption></figure>

**JSON Model:**

This dashboard is designed to provide you with comprehensive monitoring and visualization tools to effectively manage your Telepresence environment.

```json
{
  "__inputs": [
    {
      "name": "DS_PROMETHEUS",
      "label": "Prometheus",
      "description": "",
      "type": "datasource",
      "pluginId": "prometheus",
      "pluginName": "Prometheus"
    }
  ],
  "__elements": {},
  "__requires": [
    {
      "type": "panel",
      "id": "barchart",
      "name": "Bar chart",
      "version": ""
    },
    {
      "type": "grafana",
      "id": "grafana",
      "name": "Grafana",
      "version": "10.1.5"
    },
    {
      "type": "panel",
      "id": "piechart",
      "name": "Pie chart",
      "version": ""
    },
    {
      "type": "datasource",
      "id": "prometheus",
      "name": "Prometheus",
      "version": "1.0.0"
    },
    {
      "type": "panel",
      "id": "stat",
      "name": "Stat",
      "version": ""
    }
  ],
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": {
          "type": "grafana",
          "uid": "-- Grafana --"
        },
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "id": null,
  "links": [],
  "liveNow": false,
  "panels": [
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_PROMETHEUS}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          }
        },
        "overrides": []
      },
      "gridPos": {
        "h": 7,
        "w": 6,
        "x": 0,
        "y": 0
      },
      "id": 5,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "10.1.5",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_PROMETHEUS}"
          },
          "editorMode": "code",
          "exemplar": false,
          "expr": "agent_count",
          "instant": true,
          "legendFormat": "__auto",
          "range": false,
          "refId": "A"
        }
      ],
      "title": "Number of connected traffic agents",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_PROMETHEUS}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          }
        },
        "overrides": []
      },
      "gridPos": {
        "h": 7,
        "w": 6,
        "x": 6,
        "y": 0
      },
      "id": 6,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "10.1.5",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_PROMETHEUS}"
          },
          "editorMode": "code",
          "exemplar": false,
          "expr": "client_count",
          "instant": true,
          "legendFormat": "__auto",
          "range": false,
          "refId": "A"
        }
      ],
      "title": "Number of connected clients",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_PROMETHEUS}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          }
        },
        "overrides": []
      },
      "gridPos": {
        "h": 7,
        "w": 6,
        "x": 12,
        "y": 0
      },
      "id": 7,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "10.1.5",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_PROMETHEUS}"
          },
          "editorMode": "code",
          "exemplar": false,
          "expr": "active_intercept_count",
          "instant": true,
          "legendFormat": "__auto",
          "range": false,
          "refId": "A"
        }
      ],
      "title": "Number of active intercepts",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_PROMETHEUS}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "thresholds"
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          }
        },
        "overrides": []
      },
      "gridPos": {
        "h": 7,
        "w": 6,
        "x": 18,
        "y": 0
      },
      "id": 8,
      "options": {
        "colorMode": "value",
        "graphMode": "area",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "textMode": "auto"
      },
      "pluginVersion": "10.1.5",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_PROMETHEUS}"
          },
          "editorMode": "code",
          "exemplar": false,
          "expr": "session_count",
          "instant": true,
          "legendFormat": "__auto",
          "range": false,
          "refId": "A"
        }
      ],
      "title": "Number of sessions",
      "type": "stat"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_PROMETHEUS}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "fixedColor": "light-orange",
            "mode": "shades"
          },
          "custom": {
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            }
          },
          "mappings": []
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 7
      },
      "id": 3,
      "interval": "15s",
      "options": {
        "displayLabels": [
          "value"
        ],
        "legend": {
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": true,
          "values": [
            "value"
          ]
        },
        "pieType": "pie",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "tooltip": {
          "mode": "single",
          "sort": "none"
        }
      },
      "pluginVersion": "10.1.5",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_PROMETHEUS}"
          },
          "editorMode": "code",
          "exemplar": false,
          "expr": "round(sum(increase(connect_count[$__range])) by (client, install_id))",
          "instant": true,
          "legendFormat": "__auto",
          "range": false,
          "refId": "A"
        }
      ],
      "title": "Total number of connects",
      "type": "piechart"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_PROMETHEUS}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "fixedColor": "light-blue",
            "mode": "shades"
          },
          "custom": {
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            }
          },
          "mappings": []
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 7
      },
      "id": 4,
      "options": {
        "displayLabels": [
          "value"
        ],
        "legend": {
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": true,
          "values": [
            "value"
          ]
        },
        "pieType": "pie",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "tooltip": {
          "mode": "single",
          "sort": "none"
        }
      },
      "pluginVersion": "10.1.5",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_PROMETHEUS}"
          },
          "editorMode": "code",
          "exemplar": false,
          "expr": "round(sum(increase(intercept_count[$__range])) by (client, install_id))",
          "instant": true,
          "legendFormat": "__auto",
          "range": false,
          "refId": "A"
        }
      ],
      "title": "Total number of intercepts",
      "type": "piechart"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_PROMETHEUS}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "fixedColor": "light-purple",
            "mode": "shades"
          },
          "custom": {
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            }
          },
          "mappings": []
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 15
      },
      "id": 10,
      "options": {
        "displayLabels": [
          "value"
        ],
        "legend": {
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": true,
          "values": [
            "value"
          ]
        },
        "pieType": "pie",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "tooltip": {
          "mode": "single",
          "sort": "none"
        }
      },
      "pluginVersion": "10.1.5",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_PROMETHEUS}"
          },
          "editorMode": "code",
          "exemplar": false,
          "expr": "round(sum(increase(intercept_count{intercept_type=\"personal\"}[$__range])) by (client, install_id))",
          "instant": true,
          "legendFormat": "__auto",
          "range": false,
          "refId": "A"
        }
      ],
      "title": "Total number of personal intercepts",
      "type": "piechart"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_PROMETHEUS}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "fixedColor": "super-light-red",
            "mode": "shades"
          },
          "custom": {
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            }
          },
          "mappings": []
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 15
      },
      "id": 9,
      "options": {
        "displayLabels": [
          "value"
        ],
        "legend": {
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": true,
          "values": [
            "value"
          ]
        },
        "pieType": "pie",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": false
        },
        "tooltip": {
          "mode": "single",
          "sort": "none"
        }
      },
      "pluginVersion": "10.1.5",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_PROMETHEUS}"
          },
          "editorMode": "code",
          "exemplar": false,
          "expr": "round(sum(increase(intercept_count{intercept_type=\"global\"}[$__range])) by (client, install_id))",
          "instant": true,
          "legendFormat": "__auto",
          "range": false,
          "refId": "A"
        }
      ],
      "title": "Total number of global intercepts",
      "type": "piechart"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_PROMETHEUS}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "continuous-YlBl"
          },
          "custom": {
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "fillOpacity": 80,
            "gradientMode": "none",
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            },
            "lineWidth": 1,
            "scaleDistribution": {
              "type": "linear"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          }
        },
        "overrides": []
      },
      "gridPos": {
        "h": 13,
        "w": 12,
        "x": 0,
        "y": 23
      },
      "id": 2,
      "options": {
        "barRadius": 0,
        "barWidth": 0.97,
        "fullHighlight": false,
        "groupWidth": 0.7,
        "legend": {
          "calcs": [
            "last"
          ],
          "displayMode": "table",
          "placement": "bottom",
          "showLegend": true
        },
        "orientation": "auto",
        "showValue": "auto",
        "stacking": "none",
        "tooltip": {
          "mode": "single",
          "sort": "none"
        },
        "xTickLabelRotation": 0,
        "xTickLabelSpacing": 0
      },
      "pluginVersion": "10.1.5",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_PROMETHEUS}"
          },
          "editorMode": "code",
          "exemplar": false,
          "expr": "(avg_over_time(sum by (client, install_id) (connect_active_status)[$__range:])) * $__range_s / 60",
          "instant": true,
          "legendFormat": "__auto",
          "range": false,
          "refId": "A"
        }
      ],
      "title": "Connects duration in minutes",
      "type": "barchart"
    },
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_PROMETHEUS}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "fixedColor": "text",
            "mode": "continuous-RdYlGr"
          },
          "custom": {
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "fillOpacity": 80,
            "gradientMode": "none",
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            },
            "lineWidth": 1,
            "scaleDistribution": {
              "type": "linear"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          }
        },
        "overrides": []
      },
      "gridPos": {
        "h": 13,
        "w": 12,
        "x": 12,
        "y": 23
      },
      "id": 1,
      "options": {
        "barRadius": 0,
        "barWidth": 0.97,
        "fullHighlight": false,
        "groupWidth": 0.7,
        "legend": {
          "calcs": [
            "last"
          ],
          "displayMode": "table",
          "placement": "bottom",
          "showLegend": true
        },
        "orientation": "auto",
        "showValue": "auto",
        "stacking": "none",
        "tooltip": {
          "mode": "single",
          "sort": "none"
        },
        "xTickLabelRotation": 0,
        "xTickLabelSpacing": 0
      },
      "pluginVersion": "10.1.5",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_PROMETHEUS}"
          },
          "editorMode": "code",
          "exemplar": false,
          "expr": "(avg_over_time(sum by (client, install_id) (intercept_active_status)[$__range:])) * $__range_s / 60",
          "instant": true,
          "legendFormat": "__auto",
          "range": false,
          "refId": "A"
        }
      ],
      "title": "Intercepts duration in minutes",
      "type": "barchart"
    }
  ],
  "refresh": "",
  "schemaVersion": 38,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-30d",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "Telepresence",
  "uid": "d99c884a-8f4f-43f8-bd4e-bd68e47f100d",
  "version": 5,
  "weekStart": ""
}
```
