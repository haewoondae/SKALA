apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${USER_NAME}-${SERVICE_NAME}
  namespace: ${NAMESPACE}
  annotations:
    prometheus.io/scrape: 'true'
    prometheus.io/port: '8081'
    prometheus.io/path: '/actuator/prometheus'
    update: 7a4d145eaf266c9c6f556cce11c1c6f0
  labels:
    app: ${USER_NAME}-${SERVICE_NAME}
spec:
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: ${USER_NAME}-${SERVICE_NAME}
  template:
    metadata:
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8081'
        prometheus.io/path: '/actuator/prometheus'
      labels:
        app: ${USER_NAME}-${SERVICE_NAME}
    spec:
      serviceAccountName: default
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: ${TAINT_KEY}
                operator: In
                values:
                - "${TAINT_VALUE}"
      tolerations:
      - effect: ${TAINT_EFFECT}
        key: ${TAINT_KEY}
        operator: Equal
        value: "${TAINT_VALUE}"
      containers:
      - name: webserver
        image: ${DOCKER_REGISTRY}/${USER_NAME}-${IMAGE_NAME}:${VERSION}
        imagePullPolicy: Always
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
      volumes:
      - name: config-volume
        configMap:
          name: ${PROFILE}-file-config

