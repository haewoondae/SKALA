apiVersion: v1
kind: PersistentVolume
metadata:
  name: efs-${SERVICE_NAME}
spec:
  capacity:
    storage: 100Mi  # 논리적 크기, 실제 EFS는 무제한
  volumeMode: Filesystem
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  csi:
    driver: efs.csi.aws.com
    volumeHandle: fs-0e24afe9e2bc46ee5::fsap-066c4369ed1b14b8f # AWS EFS 파일 시스템 ID
  claimRef:
    namespace: ${NAMESPACE}
    name: efs-${SERVICE_NAME}

