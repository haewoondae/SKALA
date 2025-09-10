apiVersion: v1
kind: Endpoints
metadata:
  name: ${USER_NAME}-replicaset-test
  namespace: skala-practice
subsets:
  - addresses:
      - ip: 10.244.1.23   # 실제 Pod IP
      - ip: 10.244.2.45   # 다른 Pod IP
    ports:
      - name: http
        port: 8080
        protocol: TCP
      - name: mgmt
        port: 8081
        protocol: TCP

