package com.skala.basic.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.skala.basic.data.HelloRequest;
import com.skala.basic.data.HelloResponse;
import com.skala.basic.service.HelloService;

import jakarta.validation.Valid;

@RestController
public class HelloController {
    
    // Logger 선언
    private static final Logger log = LoggerFactory.getLogger(HelloController.class);
    
    // HelloService 의존성 주입을 위한 필드
    private final HelloService helloService;
    
    // 생성자 주입
    public HelloController(HelloService helloService) {
        this.helloService = helloService;
    }
    
    @GetMapping("/hello")
    public HelloResponse hello(@RequestParam(defaultValue = "SKALA") String name) {
        // 서비스 호출하여 응답 객체 생성
        log.info("/hello: GET {}", name);
        return helloService.createMessage(name);
    }
    
    @PostMapping("/hello")
    public HelloResponse postHello(@Valid @RequestBody HelloRequest body) {
        log.info("/hello: POST {}", body.getName());
        return helloService.createMessage(body.getName());
    }
}