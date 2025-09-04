package com.skala.basic.service;

import org.springframework.stereotype.Service;

import com.skala.basic.data.HelloRequest;
import com.skala.basic.data.HelloResponse;

@Service
public class HelloService {

    // 기존 메서드 (String name용)
    public HelloResponse createMessage(String name) {
        HelloResponse response = new HelloResponse();
        response.setMessage("안녕하세요, " + name + "님!");
        return response;
    }
    
    // 새로 추가해야 할 메서드 (HelloRequest용)
    public HelloResponse createMessageFromRequest(HelloRequest request) {
        HelloResponse response = new HelloResponse();
        // HelloRequest의 name, email, age 정보를 활용한 메시지 생성
        String message = String.format("안녕하세요, %s님! 이메일: %s, 나이: %d세", 
                                      request.getName(), 
                                      request.getEmail(), 
                                      request.getAge());
        response.setMessage(message);
        return response;
    }
}