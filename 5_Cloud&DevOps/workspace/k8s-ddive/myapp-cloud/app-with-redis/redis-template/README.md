# Redis Key-Value API

Spring Boot와 Lettuce를 사용한 Redis Key-Value 관리 API입니다.

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [기술 스택](#기술-스택)
- [설치 및 실행](#설치-및-실행)
- [API 엔드포인트](#api-엔드포인트)
- [사용 예시](#사용-예시)
- [응답 형태](#응답-형태)

## 🚀 프로젝트 개요

이 프로젝트는 Redis 데이터베이스에 Key-Value 쌍을 저장, 조회, 삭제할 수 있는 RESTful API를 제공합니다.

## 🛠 기술 스택

- **Java 17**
- **Spring Boot 3.2.6**
- **Spring Data Redis**
- **Lettuce Core 6.5.5**
- **Lombok**
- **Maven**

## ⚙️ 설치 및 실행

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd redis-hello-demo
```

### 2. Redis 서버 설정
`application.yml` 또는 `application.properties`에 Redis 연결 정보를 설정하세요:

```yaml
spring:
  redis:
    host: localhost
    port: 6379
    username: your-username
    password: your-password
```

### 3. 애플리케이션 실행
```bash
mvn spring-boot:run
```

서버는 기본적으로 `http://localhost:8080`에서 실행됩니다.

## 📚 API 엔드포인트

### 1. Key-Value 저장

#### 방법 1: Query Parameter 방식
```http
POST /redis/key-value?key=mykey&value=myvalue
```

#### 방법 2: JSON 방식
```http
POST /redis/json
Content-Type: application/json

{
  "key": "mykey",
  "value": "myvalue"
}
```

### 2. Value 조회
```http
GET /redis/{key}
```
**예시:** `GET /redis/mykey`

### 3. Key 삭제
```http
DELETE /redis/{key}
```
**예시:** `DELETE /redis/mykey`

### 4. Key 존재 여부 확인
```http
GET /redis/exists/{key}
```
**예시:** `GET /redis/exists/mykey`

### 5. 테스트 엔드포인트
```http
GET /redis/test     # HELLO + MapOutput 사용
GET /redis/test2    # AUTH 분리 방식
GET /redis/test3    # HELLO 없이 AUTH만
```

## 💡 사용 예시

### cURL을 사용한 테스트

#### 1. 값 저장 (Query Parameter 방식)
```bash
curl -X POST "http://localhost:8080/redis/set?key=username&value=john"
```

#### 2. 값 저장 (JSON 방식)
```bash
curl -X POST "http://localhost:8080/redis/set-json" \
  -H "Content-Type: application/json" \
  -d '{"key":"email","value":"john@example.com"}'
```

#### 3. 값 조회
```bash
curl -X GET "http://localhost:8080/redis/get/username"
```

#### 4. 키 삭제
```bash
curl -X DELETE "http://localhost:8080/redis/delete/username"
```

#### 5. 키 존재 확인
```bash
curl -X GET "http://localhost:8080/redis/exists/username"
```

### Postman 사용 예시

1. **POST** `/redis/set`
   - Params: `key=test`, `value=hello`

2. **POST** `/redis/set-json`
   - Body (JSON):
     ```json
     {
       "key": "user:1",
       "value": "John Doe"
     }
     ```

3. **GET** `/redis/get/test`

4. **DELETE** `/redis/delete/test`

5. **GET** `/redis/exists/test`

## 📝 응답 형태

### 성공 응답
```json
HTTP/1.1 200 OK
Content-Type: text/plain

키 'username'에 값 'john' 저장 완료: OK
```

### 에러 응답
```json
HTTP/1.1 500 Internal Server Error
Content-Type: text/plain

에러 발생: Connection refused
```

### 404 응답 (키를 찾을 수 없는 경우)
```json
HTTP/1.1 404 Not Found
Content-Type: text/plain

키 'nonexistent'를 찾을 수 없습니다.
```

## 🔧 주요 기능

- ✅ **Redis 연결 및 인증 처리**
- ✅ **Key-Value 저장/조회/삭제**
- ✅ **Key 존재 여부 확인**
- ✅ **RESTful API 설계**
- ✅ **에러 처리 및 적절한 HTTP 상태 코드**
- ✅ **Query Parameter 및 JSON 방식 모두 지원**
- ✅ **한글 응답 메시지**

## 🐛 문제 해결

### Redis 연결 문제
- Redis 서버가 실행 중인지 확인
- `application.yml`의 연결 정보 확인
- 방화벽 설정 확인

### 인증 문제
- Username과 Password가 올바른지 확인
- Redis ACL 설정 확인

## 📄 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다.
