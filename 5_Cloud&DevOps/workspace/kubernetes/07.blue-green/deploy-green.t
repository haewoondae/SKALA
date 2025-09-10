apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${USER_NAME}-${SERVICE_NAME}-new
  namespace: ${NAMESPACE}
spec:
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: ${USER_NAME}-${SERVICE_NAME}-new
  template:
    metadata:
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8080'
        prometheus.io/path: '/actuator/prometheus'
        update: ${HASHCODE}
      labels:
        app: ${USER_NAME}-${SERVICE_NAME}-new
    spec:
      serviceAccountName: default
      containers:
      - name: ${IMAGE_NAME}
        image: ${DOCKER_REGISTRY}/${USER_NAME}-${IMAGE_NAME}-new:2.0.0-NEW
        imagePullPolicy: Always
        env:
        - name: USER_NAME
          value: ${USER_NAME}
        - name: NAMESPACE
          value: ${NAMESPACE}
