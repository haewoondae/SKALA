package com.example.redis;

import io.lettuce.core.RedisClient;
import io.lettuce.core.api.StatefulRedisConnection;
import io.lettuce.core.api.sync.RedisCommands;
import io.lettuce.core.codec.StringCodec;
import io.lettuce.core.output.MapOutput;
import io.lettuce.core.protocol.CommandArgs;
import io.lettuce.core.protocol.CommandType;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import lombok.extern.slf4j.Slf4j;

import java.util.Map;

@Slf4j
@Service
public class RedisService {

    private final RedisClient redisClient;
    private final CommandArgs<String, String> helloCommandArgs;

    public RedisService(RedisClient redisClient,
                        CommandArgs<String, String> helloCommandArgs) {
        this.redisClient = redisClient;
        this.helloCommandArgs = helloCommandArgs;
    }

    public String helloAndSet() {
        try (StatefulRedisConnection<String, String> conn = redisClient.connect()) {

            RedisCommands<String, String> cmd = conn.sync();

            // RedisConfig에서 설정한 CommandArgs 사용
            Map<String, String> helloResponse = cmd.dispatch(
                    CommandType.HELLO,
                    new MapOutput<>(StringCodec.UTF8),
                    helloCommandArgs
            );

            //log.debug("HELLO 응답: {}", helloResponse);

            return cmd.set("spring:hello", "world"); // "OK" 예상
        }
    }


    // Key-Value 추가 기능
    public String setValue(String key, String value) {
        try (StatefulRedisConnection<String, String> conn = redisClient.connect()) {
            RedisCommands<String, String> cmd = conn.sync();

            // RedisConfig에서 인증 설정이 되어있으므로 별도 인증 불필요
            return cmd.set(key, value);
        }
    }

    // Key로 값 조회 기능
    public String getValue(String key) {
        try (StatefulRedisConnection<String, String> conn = redisClient.connect()) {
            RedisCommands<String, String> cmd = conn.sync();

            // 별도 인증 없이 바로 GET 실행
            return cmd.get(key);
        }
    }

    // Key 삭제 기능
    public Long deleteKey(String key) {
        try (StatefulRedisConnection<String, String> conn = redisClient.connect()) {
            RedisCommands<String, String> cmd = conn.sync();

            // 별도 인증 없이 바로 DEL 실행
            return cmd.del(key);
        }
    }

    // Key 존재 여부 확인
    public Boolean existsKey(String key) {
        try (StatefulRedisConnection<String, String> conn = redisClient.connect()) {
            RedisCommands<String, String> cmd = conn.sync();

            // 별도 인증 없이 바로 EXISTS 실행
            return cmd.exists(key) > 0;
        }
    }
}
