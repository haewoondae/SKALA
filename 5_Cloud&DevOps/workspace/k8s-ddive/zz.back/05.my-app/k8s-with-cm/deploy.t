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
      serviceAccountName: default
      volumes:
      - name: skala-config-volume
        configMap:
          name: skala-configmap
      containers:
      - name: ${IMAGE_NAME}
        image: ${DOCKER_REGISTRY}/${USER_NAME}-${IMAGE_NAME}:${VERSION}
        imagePullPolicy: Always
        volumeMounts:
        - name: skala-config-volume
          mountPath: /etc/skala
        env:
        - name: LOGGING_LEVEL
          value: ${LOGGING_LEVEL}
        - name: USER_NAME
          value: ${USER_NAME}
        - name: SKALA_INFO
          valueFrom:
            configMapKeyRef:
              name: skala-configmap
              key: skala-info
