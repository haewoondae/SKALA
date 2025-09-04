package com.sk.skala.stockapi.data.table;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "player")
public class Player {

    @Id
    private String playerId;
    
    private String playerPassword;
    
    private Double playerMoney;

    // 빈 생성자
    public Player() {
    }

    // 플레이어 ID와 초기 투자금을 인자로 받는 생성자
    public Player(String playerId, Double playerMoney) {
        this.playerId = playerId;
        this.playerMoney = playerMoney;
    }

    // Getter 메서드들
    public String getPlayerId() {
        return playerId;
    }

    public String getPlayerPassword() {
        return playerPassword;
    }

    public Double getPlayerMoney() {
        return playerMoney;
    }

    // Setter 메서드들
    public void setPlayerId(String playerId) {
        this.playerId = playerId;
    }

    public void setPlayerPassword(String playerPassword) {
        this.playerPassword = playerPassword;
    }

    public void setPlayerMoney(Double playerMoney) {
        this.playerMoney = playerMoney;
    }

    // toString 메서드 (디버깅용)
    @Override
    public String toString() {
        return "Player{" +
                "playerId='" + playerId + '\'' +
                ", playerPassword='" + playerPassword + '\'' +
                ", playerMoney=" + playerMoney +
                '}';
    }
}