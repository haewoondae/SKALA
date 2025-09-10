FROM amdp-registry.skala-ai.com/skala25a/skala-k8s.base@sha256:4318d0945c3f1bd284ff33b3f82edcc7202e8186f5bf306ed07f594b349007dc

RUN pip install psutil prometheus-client

# lifecycle (prob, healthz, metrics) 테스트를 위한 코드 추가
COPY fastserver.py fastserver.py

CMD ["python3", "fastserver.py"]

