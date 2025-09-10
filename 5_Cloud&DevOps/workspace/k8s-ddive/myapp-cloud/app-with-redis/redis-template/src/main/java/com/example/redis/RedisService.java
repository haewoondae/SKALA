package com.example.redis;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.util.Set;
import java.util.concurrent.TimeUnit;

@Slf4j
@Service
@RequiredArgsConstructor
public class RedisService {

    private final StringRedisTemplate stringRedisTemplate;
    private final RedisTemplate<String, Object> redisTemplate;

    // ========== String 타입 연산 ==========

    /**
     * 문자열 값 저장
     */
    public void setValue(String key, String value) {
        try {
            stringRedisTemplate.opsForValue().set(key, value);
            log.debug("Redis SET 성공: key={}, value={}", key, value);
        } catch (Exception e) {
            log.error("Redis SET 실패: key={}, value={}", key, value, e);
            throw new RuntimeException("Redis SET 실패", e);
        }
    }

    /**
     * 문자열 값 저장 (만료 시간 포함)
     */
    public void setValue(String key, String value, Duration timeout) {
        try {
            stringRedisTemplate.opsForValue().set(key, value, timeout);
            log.debug("Redis SET 성공 (TTL): key={}, value={}, timeout={}", key, value, timeout);
        } catch (Exception e) {
            log.error("Redis SET 실패 (TTL): key={}, value={}, timeout={}", key, value, timeout, e);
            throw new RuntimeException("Redis SET 실패", e);
        }
    }

    /**
     * 문자열 값 조회
     */
    public String getValue(String key) {
        try {
            String value = stringRedisTemplate.opsForValue().get(key);
            log.debug("Redis GET: key={}, value={}", key, value);
            return value;
        } catch (Exception e) {
            log.error("Redis GET 실패: key={}", key, e);
            throw new RuntimeException("Redis GET 실패", e);
        }
    }

    /**
     * Key 삭제
     */
    public Boolean deleteKey(String key) {
        try {
            Boolean result = stringRedisTemplate.delete(key);
            log.debug("Redis DEL: key={}, result={}", key, result);
            return result;
        } catch (Exception e) {
            log.error("Redis DEL 실패: key={}", key, e);
            throw new RuntimeException("Redis DEL 실패", e);
        }
    }

    /**
     * Key 존재 여부 확인
     */
    public Boolean existsKey(String key) {
        try {
            Boolean exists = stringRedisTemplate.hasKey(key);
            log.debug("Redis EXISTS: key={}, exists={}", key, exists);
            return exists;
        } catch (Exception e) {
            log.error("Redis EXISTS 실패: key={}", key, e);
            throw new RuntimeException("Redis EXISTS 실패", e);
        }
    }

    /**
     * Key의 만료 시간 설정 (초 단위)
     */
    public Boolean expire(String key, long timeout) {
        try {
            Boolean result = stringRedisTemplate.expire(key, timeout, TimeUnit.SECONDS);
            log.debug("Redis EXPIRE: key={}, timeout={}초, result={}", key, timeout, result);
            return result;
        } catch (Exception e) {
            log.error("Redis EXPIRE 실패: key={}, timeout={}", key, timeout, e);
            throw new RuntimeException("Redis EXPIRE 실패", e);
        }
    }

    /**
     * Key의 남은 만료 시간 조회 (초 단위)
     */
    public Long getExpire(String key) {
        try {
            Long ttl = stringRedisTemplate.getExpire(key, TimeUnit.SECONDS);
            log.debug("Redis TTL: key={}, ttl={}초", key, ttl);
            return ttl;
        } catch (Exception e) {
            log.error("Redis TTL 실패: key={}", key, e);
            throw new RuntimeException("Redis TTL 실패", e);
        }
    }

    // ========== Object 타입 연산 ==========

    /**
     * 객체 저장
     */
    public void setObject(String key, Object value) {
        try {
            redisTemplate.opsForValue().set(key, value);
            log.debug("Redis SET Object 성공: key={}, valueType={}", key, value.getClass().getSimpleName());
        } catch (Exception e) {
            log.error("Redis SET Object 실패: key={}, value={}", key, value, e);
            throw new RuntimeException("Redis SET Object 실패", e);
        }
    }

    /**
     * 객체 저장 (만료 시간 포함)
     */
    public void setObject(String key, Object value, Duration timeout) {
        try {
            redisTemplate.opsForValue().set(key, value, timeout);
            log.debug("Redis SET Object 성공 (TTL): key={}, valueType={}, timeout={}",
                    key, value.getClass().getSimpleName(), timeout);
        } catch (Exception e) {
            log.error("Redis SET Object 실패 (TTL): key={}, value={}, timeout={}", key, value, timeout, e);
            throw new RuntimeException("Redis SET Object 실패", e);
        }
    }

    /**
     * 객체 조회
     */
    public Object getObject(String key) {
        try {
            Object value = redisTemplate.opsForValue().get(key);
            log.debug("Redis GET Object: key={}, valueType={}", key,
                    value != null ? value.getClass().getSimpleName() : "null");
            return value;
        } catch (Exception e) {
            log.error("Redis GET Object 실패: key={}", key, e);
            throw new RuntimeException("Redis GET Object 실패", e);
        }
    }

    /**
     * 타입 안전한 객체 조회
     */
    @SuppressWarnings("unchecked")
    public <T> T getObject(String key, Class<T> clazz) {
        try {
            Object value = redisTemplate.opsForValue().get(key);
            if (value == null) {
                return null;
            }
            if (clazz.isInstance(value)) {
                return (T) value;
            }
            log.warn("타입 불일치: key={}, expected={}, actual={}",
                    key, clazz.getSimpleName(), value.getClass().getSimpleName());
            return null;
        } catch (Exception e) {
            log.error("Redis GET Object 실패: key={}, clazz={}", key, clazz.getSimpleName(), e);
            throw new RuntimeException("Redis GET Object 실패", e);
        }
    }

    // ========== 패턴 검색 ==========

    /**
     * 패턴으로 키 검색
     */
    public Set<String> getKeys(String pattern) {
        try {
            Set<String> keys = stringRedisTemplate.keys(pattern);
            log.debug("Redis KEYS: pattern={}, count={}", pattern, keys != null ? keys.size() : 0);
            return keys;
        } catch (Exception e) {
            log.error("Redis KEYS 실패: pattern={}", pattern, e);
            throw new RuntimeException("Redis KEYS 실패", e);
        }
    }

    // ========== 연결 테스트 ==========

    /**
     * Redis 연결 테스트
     */
    public String ping() {
        try {
            String result = stringRedisTemplate.getConnectionFactory()
                    .getConnection()
                    .ping();
            log.info("Redis PING 성공: {}", result);
            return result;
        } catch (Exception e) {
            log.error("Redis PING 실패", e);
            throw new RuntimeException("Redis 연결 실패", e);
        }
    }

    /**
     * 간단한 SET/GET 테스트
     */
    public String helloAndSet() {
        try {
            String testKey = "spring:hello";
            String testValue = "world";

            setValue(testKey, testValue);
            String retrievedValue = getValue(testKey);

            if (testValue.equals(retrievedValue)) {
                log.info("Redis 테스트 성공: key={}, value={}", testKey, retrievedValue);
                return "OK";
            } else {
                log.error("Redis 테스트 실패: expected={}, actual={}", testValue, retrievedValue);
                return "FAIL";
            }
        } catch (Exception e) {
            log.error("Redis 테스트 중 오류 발생", e);
            throw new RuntimeException("Redis 테스트 실패", e);
        }
    }
}
