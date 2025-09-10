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
        image: nginx:latest
        ports:
        - containerPort: 80

