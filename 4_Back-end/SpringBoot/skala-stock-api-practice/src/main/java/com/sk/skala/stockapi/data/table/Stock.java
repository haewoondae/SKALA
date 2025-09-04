package com.sk.skala.stockapi.data.table;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "stock")
public class Stock {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String stockName;
    
    private Double stockPrice;

    // 빈 생성자
    public Stock() {
    }

    // stockName과 stockPrice를 인자로 받는 생성자
    public Stock(String stockName, Double stockPrice) {
        this.stockName = stockName;
        this.stockPrice = stockPrice;
    }

    // Getter 메서드들
    public Long getId() {
        return id;
    }

    public String getStockName() {
        return stockName;
    }

    public Double getStockPrice() {
        return stockPrice;
    }

    // Setter 메서드들
    public void setId(Long id) {
        this.id = id;
    }

    public void setStockName(String stockName) {
        this.stockName = stockName;
    }

    public void setStockPrice(Double stockPrice) {
        this.stockPrice = stockPrice;
    }

    // toString 메서드 (디버깅용)
    @Override
    public String toString() {
        return "Stock{" +
                "id=" + id +
                ", stockName='" + stockName + '\'' +
                ", stockPrice=" + stockPrice +
                '}';
    }
}