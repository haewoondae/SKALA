apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${USER_NAME}-ingress
  namespace: ${NAMESPACE}
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  ingressClassName: public-nginx
  rules:
  - host: ${USER_NAME}-tls.skala25a.project.skala-ai.com
    http:
      paths:
      - backend:
          service:
            name: ${USER_NAME}-${SERVICE_NAME}
            port:
              number: 8080
        path: /api
        pathType: Prefix
      - backend:
          service:
            name: ${USER_NAME}-${SERVICE_NAME}
            port:
              number: 8081
        path: /actuator
        pathType: Prefix
      - backend:
          service:
            name: ${USER_NAME}-${SERVICE_NAME}
            port:
              number: 8080
        path: /swagger
        pathType: Prefix
      - backend:
          service:
            name: ${USER_NAME}-${SERVICE_NAME}
            port:
              number: 8080
        path: /${USER_NAME}(/|$)(.*)
        pathType: ImplementationSpecific
