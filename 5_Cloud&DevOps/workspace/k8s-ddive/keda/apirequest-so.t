apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: ${USER_NAME}-api-so
  namespace: skala-practice
spec:
  scaleTargetRef:
    kind: Deployment
    name: ${USER_NAME}-my-app
  pollingInterval: 5              
  cooldownPeriod: 10              
  minReplicaCount: 1
  maxReplicaCount: 10
  advanced:
    horizontalPodAutoscalerConfig:
      behavior:
        scaleUp:
          stabilizationWindowSeconds: 0
          policies:
          - type: Percent
            value: 100
            periodSeconds: 5
        scaleDown:
          stabilizationWindowSeconds: 0
          policies:
          - type: Percent
            value: 100
            periodSeconds: 5

  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus-server.remote-rde:80  # 실제 Prometheus 주소로 변경
      metricName: http_requests_per_second
      query: >
        avg(rate(http_server_requests_seconds_count{namespace="skala-practice", pod=~"${USER_NAME}-my-app-.*"}[1m]))
      threshold: "10"  
