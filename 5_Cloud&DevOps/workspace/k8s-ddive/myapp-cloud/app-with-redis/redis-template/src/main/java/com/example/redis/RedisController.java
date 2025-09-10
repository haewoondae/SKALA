package com.example.redis;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/redis")
public class RedisController {

    private final RedisService redisService;

    public RedisController(RedisService redisService) {
        this.redisService = redisService;
    }

    @GetMapping("/test")
    public ResponseEntity<String> test() {
        String result = redisService.helloAndSet(); // 예상 결과 "OK"
        return ResponseEntity.ok("Redis SET 결과: " + result);
    }

    // Key-Value 추가 (POST)
    @PostMapping("/key-value")
    public ResponseEntity<String> setValue(@RequestParam String key, @RequestParam String value) {
        try {
            redisService.setValue(key, value);
            return ResponseEntity.ok("키 '" + key + "'에 값 '" + value + "' 저장 완료: " + redisService.getValue(key));
        } catch (Exception e) {
            return ResponseEntity.status(500).body("에러 발생: " + e.getMessage());
        }
    }

    // Key-Value 추가 (JSON 방식)
    @PostMapping("/json")
    public ResponseEntity<String> setValueJson(@RequestBody KeyValueRequest request) {
        try {
            redisService.setValue(request.getKey(), request.getValue());
            return ResponseEntity.ok("키 '" + request.getKey() + "'에 값 '" + request.getValue() + "' 저장 완료: " + redisService.getValue(request.getKey()));
        } catch (Exception e) {
            return ResponseEntity.status(500).body("에러 발생: " + e.getMessage());
        }
    }

    // Key로 값 조회 (GET)
    @GetMapping("/{key}")
    public ResponseEntity<String> getValue(@PathVariable String key) {
        try {
            String value = redisService.getValue(key);
            if (value != null) {
                return ResponseEntity.ok("키 '" + key + "'의 값: " + value);
            } else {
                return ResponseEntity.status(404).body("키 '" + key + "'를 찾을 수 없습니다.");
            }
        } catch (Exception e) {
            return ResponseEntity.status(500).body("에러 발생: " + e.getMessage());
        }
    }

    // Key 삭제 (DELETE)
    @DeleteMapping("/{key}")
    public ResponseEntity<String> deleteKey(@PathVariable String key) {
        try {
            Boolean deleted = redisService.deleteKey(key);
            if (deleted) {
                return ResponseEntity.ok("키 '" + key + "' 삭제 완료");
            } else {
                return ResponseEntity.status(404).body("키 '" + key + "'를 찾을 수 없습니다.");
            }
        } catch (Exception e) {
            return ResponseEntity.status(500).body("에러 발생: " + e.getMessage());
        }
    }

    // Key 존재 여부 확인 (GET)
    @GetMapping("/exists/{key}")
    public ResponseEntity<String> existsKey(@PathVariable String key) {
        try {
            Boolean exists = redisService.existsKey(key);
            return ResponseEntity.ok("키 '" + key + "' 존재 여부: " + exists);
        } catch (Exception e) {
            return ResponseEntity.status(500).body("에러 발생: " + e.getMessage());
        }
    }
}
