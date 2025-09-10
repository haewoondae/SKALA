apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${USER_NAME}-${SERVICE_NAME}
  namespace: ${NAMESPACE}
spec:
  replicas: ${REPLICAS}
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
        - name: efs-volume
          mountPath: /data
      volumes:
      - name: efs-volume
        persistentVolumeClaim:
          claimName: ${USER_NAME}-efs-sc-${SERVICE_NAME}

