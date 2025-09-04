package com.sk.skala.stockapi.data.dto;

public class PlayerStockDto {

    private Long stockId;
    private String stockName;
    private Double stockPrice;
    private Integer quantity;

    // 빈 생성자
    public PlayerStockDto() {
    }

    // Private 생성자 (Builder 패턴용)
    private PlayerStockDto(Builder builder) {
        this.stockId = builder.stockId;
        this.stockName = builder.stockName;
        this.stockPrice = builder.stockPrice;
        this.quantity = builder.quantity;
    }

    // Getter 메서드들
    public Long getStockId() {
        return stockId;
    }

    public String getStockName() {
        return stockName;
    }

    public Double getStockPrice() {
        return stockPrice;
    }

    public Integer getQuantity() {
        return quantity;
    }

    // Setter 메서드들
    public void setStockId(Long stockId) {
        this.stockId = stockId;
    }

    public void setStockName(String stockName) {
        this.stockName = stockName;
    }

    public void setStockPrice(Double stockPrice) {
        this.stockPrice = stockPrice;
    }

    public void setQuantity(Integer quantity) {
        this.quantity = quantity;
    }

    // Builder 패턴을 위한 정적 메서드
    public static Builder builder() {
        return new Builder();
    }

    // Builder 클래스
    public static class Builder {
        private Long stockId;
        private String stockName;
        private Double stockPrice;
        private Integer quantity;

        // 메서드 체이닝을 위한 Builder 메서드들
        public Builder stockId(Long stockId) {
            this.stockId = stockId;
            return this;
        }

        public Builder stockName(String stockName) {
            this.stockName = stockName;
            return this;
        }

        public Builder stockPrice(Double stockPrice) {
            this.stockPrice = stockPrice;
            return this;
        }

        public Builder quantity(Integer quantity) {
            this.quantity = quantity;
            return this;
        }

        // 최종 객체 생성
        public PlayerStockDto build() {
            return new PlayerStockDto(this);
        }
    }

    // toString 메서드 (디버깅용)
    @Override
    public String toString() {
        return "PlayerStockDto{" +
                "stockId=" + stockId +
                ", stockName='" + stockName + '\'' +
                ", stockPrice=" + stockPrice +
                ", quantity=" + quantity +
                '}';
    }
}