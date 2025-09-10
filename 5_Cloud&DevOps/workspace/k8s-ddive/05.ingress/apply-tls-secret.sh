#!/bin/bash

USER_NAME=sk000

kubectl create secret tls ${USER_NAME}-manual-tls-secret \
  --cert=tls.crt \
  --key=tls.key \
  -n skala-practice
