package com.sk.skala.stockapi.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.sk.skala.stockapi.data.table.Stock;

public interface StockRepository extends JpaRepository<Stock, Long> {
    
    // 주식 이름으로 주식 데이터 조회 (존재 여부 확인 목적)
    Optional<Stock> findByStockName(String stockName);
}