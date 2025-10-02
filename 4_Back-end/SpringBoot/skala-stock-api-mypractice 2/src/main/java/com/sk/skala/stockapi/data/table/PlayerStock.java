package com.sk.skala.stockapi.data.table;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "player_stock")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PlayerStock {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "player_id")
    private Player player;
    
    @ManyToOne
    @JoinColumn(name = "stock_id")
    private Stock stock;
    
    private int quantity;

    // Player와 Stock 그리고 보유 주식 수를 인자로 받는 생성자
    public PlayerStock(Player player, Stock stock, int quantity) {
        this.player = player;
        this.stock = stock;
        this.quantity = quantity;
    }
}