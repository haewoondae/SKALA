package com.sk.skala.stockapi.data.dto;

import java.util.List;

public class PlayerStockListDto {

    private String playerId;
    private Double playerMoney;
    private List<PlayerStockDto> stocks;

    // 빈 생성자
    public PlayerStockListDto() {
    }

    // Private 생성자 (Builder 패턴용)
    private PlayerStockListDto(Builder builder) {
        this.playerId = builder.playerId;
        this.playerMoney = builder.playerMoney;
        this.stocks = builder.stocks;
    }

    // Getter 메서드들
    public String getPlayerId() {
        return playerId;
    }

    public Double getPlayerMoney() {
        return playerMoney;
    }

    public List<PlayerStockDto> getStocks() {
        return stocks;
    }

    // Setter 메서드들
    public void setPlayerId(String playerId) {
        this.playerId = playerId;
    }

    public void setPlayerMoney(Double playerMoney) {
        this.playerMoney = playerMoney;
    }

    public void setStocks(List<PlayerStockDto> stocks) {
        this.stocks = stocks;
    }

    // Builder 패턴을 위한 정적 메서드
    public static Builder builder() {
        return new Builder();
    }

    // Builder 클래스
    public static class Builder {
        private String playerId;
        private Double playerMoney;
        private List<PlayerStockDto> stocks;

        // 메서드 체이닝을 위한 Builder 메서드들
        public Builder playerId(String playerId) {
            this.playerId = playerId;
            return this;
        }

        public Builder playerMoney(Double playerMoney) {
            this.playerMoney = playerMoney;
            return this;
        }

        public Builder stocks(List<PlayerStockDto> stocks) {
            this.stocks = stocks;
            return this;
        }

        // 최종 객체 생성
        public PlayerStockListDto build() {
            return new PlayerStockListDto(this);
        }
    }

    // toString 메서드 (디버깅용)
    @Override
    public String toString() {
        return "PlayerStockListDto{" +
                "playerId='" + playerId + '\'' +
                ", playerMoney=" + playerMoney +
                ", stocks=" + stocks +
                '}';
    }
}