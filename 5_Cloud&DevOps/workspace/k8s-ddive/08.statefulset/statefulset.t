apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ${USER_NAME}-${SERVICE_NAME}
  namespace: ${NAMESPACE}
spec:
  replicas: ${REPLICAS}
  serviceName: ${USER_NAME}-${SERVICE_NAME}-headless
  selector:
    matchLabels:
      app: ${USER_NAME}-${SERVICE_NAME}
  template:
    metadata:
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8081'
        prometheus.io/path: '/actuator/prometheus'
        update: ${HASHCODE}
      labels:
        app: ${USER_NAME}-${SERVICE_NAME}
    spec:
      serviceAccountName: default
      containers:
      - name: ${IMAGE_NAME}
        image: ${DOCKER_REGISTRY}/${USER_NAME}-${IMAGE_NAME}:${VERSION}
        imagePullPolicy: Always
        env:
        - name: LOGGING_LEVEL
          value: ${LOGGING_LEVEL}
        - name: USER_NAME
          value: ${USER_NAME}
        - name: NAMESPACE
          value: ${NAMESPACE}
        volumeMounts:
        - name: data
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteMany"]
      storageClassName: efs-sc-shared
      resources:
        requests:
          storage: 100Mi
