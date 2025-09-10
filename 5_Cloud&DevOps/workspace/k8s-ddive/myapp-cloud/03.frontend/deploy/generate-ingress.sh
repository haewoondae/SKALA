#!/bin/bash

# 시작/끝 번호 설정 (3자리 유지)
START=61
END=90

# 출력 파일
OUTPUT_FILE="ingress-3.yaml"

echo "Generating $OUTPUT_FILE for sk$(printf "%03d" $START) to sk$(printf "%03d" $END) ..."

# 헤더 출력
cat > "$OUTPUT_FILE" <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/priority: "1000"
  name: frontend-test-ingress
  namespace: skala-practice
spec:
  ingressClassName: public-nginx
  rules:
  - host: frontend.skala25a.project.skala-ai.com
    http:
      paths:
      - path: /himang10
        pathType: Prefix
        backend:
          service:
            name: himang10-posts-get-service
            port:
              number: 8080
      - path: /sk000
        pathType: Prefix
        backend:
          service:
            name: sk000-posts-get
            port:
              number: 8080
EOF

# skNNN 경로 자동 생성
for i in $(seq $START $END); do
  ID=$(printf "%03d" $i)
  cat >> "$OUTPUT_FILE" <<EOF
      - path: /sk${ID}
        pathType: Prefix
        backend:
          service:
            name: sk${ID}-posts-get
            port:
              number: 8080
EOF
done

# TLS 섹션 마무리
cat >> "$OUTPUT_FILE" <<EOF
  tls:
  - hosts:
    - frontend.skala25a.project.skala-ai.com
    secretName: frontend-tls-secret
EOF

echo "$OUTPUT_FILE has been generated successfully."

