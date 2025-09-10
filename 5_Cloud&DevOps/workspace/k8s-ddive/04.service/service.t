apiVersion: v1
kind: Service
metadata:
  name: ${USER_NAME}-replicaset-test
  namespace: skala-practice
spec:
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: 8080
    - name: mgmt
      protocol: TCP
      port: 8081
      targetPort: 8081
  clusterIP: None  # 클러스터 IP 없이 Headless로 만들거나 생략 가능
