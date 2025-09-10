apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${USER_NAME}-${SERVICE_NAME}
  namespace: ${NAMESPACE}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${USER_NAME}-${SERVICE_NAME}
  template:
    metadata:
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8080'
        prometheus.io/path: '/prometheus'
        update: ${HASHCODE}
      labels:
        app: ${USER_NAME}-${SERVICE_NAME}
    spec:
      containers:
      - name: ${IMAGE_NAME}
        image: ${DOCKER_REGISTRY}/${USER_NAME}-${IMAGE_NAME}:${VERSION}
        imagePullPolicy: Always
        command:
        - /bin/sh
        - -c
        args:
        - exec python3 $EXEC_PYTHON_CODE --port $SERVER_PORT
        env:
        - name: EXEC_PYTHON_CODE
          value: fastserver.py
        - name: SERVER_PORT
          value: "8080"
        - name: LOGGING_LEVEL
          value: ${LOGGING_LEVEL}
        - name: USER_NAME
          value: ${USER_NAME}
