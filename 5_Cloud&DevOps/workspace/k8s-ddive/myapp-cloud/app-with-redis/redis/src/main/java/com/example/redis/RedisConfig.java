package com.example.redis;

import io.lettuce.core.RedisClient;
import io.lettuce.core.RedisURI;
import io.lettuce.core.codec.StringCodec;
import io.lettuce.core.protocol.CommandArgs;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RedisConfig {

    @Value("${spring.redis.protocol-version:3}")
    private int protocolVersion;

    @Bean(destroyMethod = "shutdown")
    public RedisClient redisClient(
            @Value("${spring.redis.host}") String host,
            @Value("${spring.redis.port}") int port,
            @Value("${spring.redis.username}") String username,
            @Value("${spring.redis.password}") String password) {

        RedisURI uri = RedisURI.Builder.redis(host, port)
                .withAuthentication(username, password.toCharArray())
                .withDatabase(0)
                .build();

        // lettuce-core 6.x 는 RESP2 기본, HELLO 가 필요하면 서비스단에서 dispatch
        return RedisClient.create(uri);
    }

    /**
     * HELLO 명령어용 CommandArgs Bean
     * Redis 프로토콜 버전을 설정에서 관리
     */
    @Bean
    public CommandArgs<String, String> helloCommandArgs() {
        return new CommandArgs<>(StringCodec.UTF8)
                .add(protocolVersion);
    }

    /**
     * 프로토콜 버전을 다른 곳에서도 사용할 수 있도록 Bean으로 제공
     */
    @Bean
    public Integer redisProtocolVersion() {
        return protocolVersion;
    }
}
