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
      containers:
      - name: webserver
        image: ${DOCKER_REGISTRY}/${USER_NAME}-${IMAGE_NAME}:${VERSION}
        imagePullPolicy: Always
        env:
        - name: USER_NAME
          value: ${USER_NAME}

        - name: DATABASE_URL
          valueFrom:
            configMapKeyRef:
              name: ${PROFILE}-db-config
              key: database.url
        - name: DATABASE_USER
          valueFrom:
            configMapKeyRef:
              name: ${PROFILE}-db-config
              key: database.user
        - name: DATABASE_PASSWORD
          valueFrom:
            configMapKeyRef:
              name: ${PROFILE}-db-config
              key: database.password

