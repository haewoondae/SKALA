package com.sk.skala.stockapi.data.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TransactionDto {

    private Long id;
    private String playerId;
    private Long stockId;
    private String stockName;
    private String transactionType; // BUY, SELL
    private int quantity;
    private double price;
    private double totalAmount;
    private LocalDateTime transactionTime;
}
