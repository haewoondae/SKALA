apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${USER_NAME}-green
  namespace: ${NAMESPACE}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${USER_NAME}-${SERVICE_NAME}
      version: ${VERSION}
  template:
    metadata:
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8081'
        prometheus.io/path: '/actuator/prometheus'
        update: ${HASHCODE}
      labels:
        app: ${USER_NAME}-${SERVICE_NAME}
        version: ${VERSION}
    spec:
      containers:
      - name: ${IMAGE_NAME}
        image: ${DOCKER_REGISTRY}/skala-${IMAGE_NAME}:${VERSION}
        imagePullPolicy: Always
        env:
        - name: LOGGING_LEVEL
          value: ${LOGGING_LEVEL}
        - name: USER_NAME
          value: ${USER_NAME}
        - name: NAMESPACE
          value: ${NAMESPACE}
