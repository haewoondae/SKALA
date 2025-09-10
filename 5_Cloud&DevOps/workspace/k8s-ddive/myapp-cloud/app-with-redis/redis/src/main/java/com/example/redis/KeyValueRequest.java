package com.example.redis;

public class KeyValueRequest {
    private String key;
    private String value;

    // 기본 생성자
    public KeyValueRequest() {}

    // 생성자
    public KeyValueRequest(String key, String value) {
        this.key = key;
        this.value = value;
    }

    // Getter, Setter
    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
}
