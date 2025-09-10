apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${USER_NAME}-attach-my-pod
  namespace: skala-practice
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${USER_NAME}-attach-my-pod
      version: "1.0.0"
  template:
    metadata:
      labels:
        app: ${USER_NAME}-attach-my-pod
        version: "1.0.0"
    spec:
      containers:
      - name: explorer
        image: ubuntu:20.04
        command: ["sleep"]
        args: ["infinity"]
        env:
        - name: USERNAME
          value: "username"
        - name: PASSWORD
          value: "password"
        volumeMounts:
        # PVC 마운트
        - name: shared-storage
          mountPath: /shared-data
      volumes:
      # PVC 볼륨 정의
      - name: shared-storage
        persistentVolumeClaim:
          claimName: my-pvc

