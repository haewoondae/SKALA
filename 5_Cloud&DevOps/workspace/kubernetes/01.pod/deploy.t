apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${USER_NAME}-deploy-test
  namespace: skala-practice
  labels:
    app: ${USER_NAME}-deploy-test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${USER_NAME}-deploy-test
  template:
    metadata:
      labels:
        app: ${USER_NAME}-deploy-test
    spec:
      serviceAccountName: default
      containers:
        - name: nginx
          image: nginx:mainline-alpine
          imagePullPolicy: Always
          env:
            - name: USER_NAME
              value: ${USER_NAME}

