package com.sk.skala.stockapi.data.table;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import java.time.LocalDateTime;

@Entity
@Table(name = "watchlist")
public class Watchlist {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "player_id")
    private Player player;
    
    @ManyToOne
    @JoinColumn(name = "stock_id")
    private Stock stock;
    
    private LocalDateTime addedTime;

    // 빈 생성자
    public Watchlist() {
    }

    // 플레이어, 주식, 추가 시간을 받는 생성자
    public Watchlist(Player player, Stock stock, LocalDateTime addedTime) {
        this.player = player;
        this.stock = stock;
        this.addedTime = addedTime;
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

    public LocalDateTime getAddedTime() {
        return addedTime;
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

    public void setAddedTime(LocalDateTime addedTime) {
        this.addedTime = addedTime;
    }

    // toString 메서드 (디버깅용)
    @Override
    public String toString() {
        return "Watchlist{" +
                "id=" + id +
                ", player=" + (player != null ? player.getPlayerId() : null) +
                ", stock=" + (stock != null ? stock.getStockName() : null) +
                ", addedTime=" + addedTime +
                '}';
    }
}
