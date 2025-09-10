#!/bin/bash

USER_NAME=sk000


# 1년짜리 self-signed 인증서 생성
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key \
  -out tls.crt \
  -subj "/CN=${USER_NAME}-tls.skala25a.project.skala-ai.com/O=com.sk.skala"

openssl x509 -in tls.crt -text -noout
