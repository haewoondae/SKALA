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
        update: ${HASHCODE}
      labels:
        app: ${USER_NAME}-${SERVICE_NAME}
    spec:
      serviceAccountName: default
      containers:
      - name: storage-test
        image: busybox
        imagePullPolicy: IfNotPresent
        command: ["/bin/sh", "-c"]
        args:
          - echo "Hello from busybox" > /data/hello.txt && sleep infinity
        volumeMounts:
        - name: emptydir-volume
          mountPath: /data
      volumes:
      - name: emptydir-volume
        emptyDir: {}

