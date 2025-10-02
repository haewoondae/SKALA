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
import java.time.LocalDateTime;

@Entity
@Table(name = "transaction")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Transaction {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "player_id")
    private Player player;
    
    @ManyToOne
    @JoinColumn(name = "stock_id")
    private Stock stock;
    
    private String transactionType; // BUY, SELL
    private int quantity;
    private double price;
    private double totalAmount; // quantity * price
    private LocalDateTime transactionTime;

    // 매매 기록 생성을 위한 생성자
    public Transaction(Player player, Stock stock, String transactionType, 
                      int quantity, double price, double totalAmount, LocalDateTime transactionTime) {
        this.player = player;
        this.stock = stock;
        this.transactionType = transactionType;
        this.quantity = quantity;
        this.price = price;
        this.totalAmount = totalAmount;
        this.transactionTime = transactionTime;
    }
}
