package com.sk.skala.stockapi.data.table;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "player_stock")
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
    
    private Integer quantity;

    // 빈 생성자
    public PlayerStock() {
    }

    // Player와 Stock 그리고 보유 주식 수를 인자로 받는 생성자
    public PlayerStock(Player player, Stock stock, Integer quantity) {
        this.player = player;
        this.stock = stock;
        this.quantity = quantity;
    }

    // Getter 메서드들
    public Long getId() {
        return id;
    }

    public Player getPlayer() {
        return player;
    }

    public Stock getStock() {
        return stock;
    }

    public Integer getQuantity() {
        return quantity;
    }

    // Setter 메서드들
    public void setId(Long id) {
        this.id = id;
    }

    public void setPlayer(Player player) {
        this.player = player;
    }

    public void setStock(Stock stock) {
        this.stock = stock;
    }

    public void setQuantity(Integer quantity) {
        this.quantity = quantity;
    }

    // toString 메서드 (디버깅용)
    @Override
    public String toString() {
        return "PlayerStock{" +
                "id=" + id +
                ", player=" + (player != null ? player.getPlayerId() : null) +
                ", stock=" + (stock != null ? stock.getStockName() : null) +
                ", quantity=" + quantity +
                '}';
    }
}