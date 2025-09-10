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
        # Secret에서 환경 변수 설정
        - name: SECRET_USERNAME
          valueFrom:
            secretKeyRef:
              name: my-secret
              key: username
        - name: SECRET_PASSWORD
          valueFrom:
            secretKeyRef:
              name: my-secret
              key: password
        volumeMounts:
        # PVC 마운트
        - name: shared-storage
          mountPath: /shared-data
        # ConfigMap을 파일로 마운트
        - name: config-volume
          mountPath: /etc/config
      volumes:
      # PVC 볼륨 정의
      - name: shared-storage
        persistentVolumeClaim:
          claimName: my-pvc
      # ConfigMap을 볼륨으로 마운트
      - name: config-volume
        configMap:
          name: my-config
      # Secret을 볼륨으로 마운트
      - name: secret-volume
        secret:
          secretName: my-secret

