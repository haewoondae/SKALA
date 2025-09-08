package com.sk.skala.stockapi.data.common;

import com.sk.skala.stockapi.config.Error;

import lombok.Data;

@Data
public class Response {
    public static final int SUCCESS = 0;
    public static final int FAIL = 1;

    private int result;
    private int code;
    private String message;
    private Object body;

    public void setError(Error error) {
        this.result = FAIL;
        this.code = error.getCode();
        this.message = error.getMessage();
    }

    public void setError(int code, String message) {
        this.result = FAIL;
        this.code = code;
        this.message = message;
    }
    
    // 컨트롤러에서 사용하는 편의 메소드들 추가
    public static Response success(Object data) {
        Response response = new Response();
        response.result = SUCCESS;
        response.code = 0;
        response.message = "성공";
        response.body = data;
        return response;
    }
    
    public static Response error(String message) {
        Response response = new Response();
        response.result = FAIL;
        response.code = -1;
        response.message = message;
        return response;
    }
    
    public static Response error(Error error) {
        Response response = new Response();
        response.setError(error);
        return response;
    }
}