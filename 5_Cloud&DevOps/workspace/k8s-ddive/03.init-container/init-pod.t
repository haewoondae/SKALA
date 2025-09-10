apiVersion: v1
kind: Pod
metadata:
  name: ${USER_NAME}-${SERVICE_NAME}
  namespace: ${NAMESPACE}
  annotations:
    prometheus.io/scrape: 'true'
    prometheus.io/port: '8081'
    prometheus.io/path: '/actuator/prometheus'
    update: ${ANNOTATION_UPDATE}
  labels:
    app: ${USER_NAME}-${SERVICE_NAME}
spec:
  initContainers:
  - name: check-active-enabled
    image: busybox
    command:
    - sh
    - -c
    - |
      timeout 300 sh -c "
      while [ ! -f /root/active.enabled ]; do
        echo 'Waiting for active.enabled file...'
        sleep 5
      done
      echo 'File active.enabled found. Initialization complete.'
      "
    volumeMounts:
    - name: root-volume
      mountPath: /root
  containers:
  - name: ${SERVICE_NAME}
    image: ${DOCKER_REGISTRY}/${USER_NAME}-${IMAGE_NAME}:${VERSION}
    imagePullPolicy: Always
    readinessProbe:
      exec:
        command:
        - sh
        - -c
        - "[ -f /root/active.enabled ]"
      initialDelaySeconds: 30
      periodSeconds: 10
    env:
    - name: LOGGING_LEVEL
      value: ${LOGGING_LEVEL}
    - name: USER_NAME
      value: ${USER_NAME}
    volumeMounts:
    - name: root-volume
      mountPath: /root
  volumes:
  - name: root-volume
    emptyDir: {}
