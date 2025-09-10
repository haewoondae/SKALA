#!/bin/bash
NAME=sk000
IMAGE_NAME="webserver"
VERSION="2.0.0"

# Docker 이미지 빌드
docker buildx build \
  --tag ${NAME}-${IMAGE_NAME}:${VERSION} \
  --file Dockerfile \
  ${IS_CACHE} .
