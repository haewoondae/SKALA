package com.sk.skala.stockapi.data.table;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "player")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Player {

    @Id
    private String playerId;
    
    private String playerPassword;
    
    private double playerMoney;

    // 플레이어 ID와 초기 투자금을 인자로 받는 생성자
    public Player(String playerId, double playerMoney) {
        this.playerId = playerId;
        this.playerMoney = playerMoney;
    }
}