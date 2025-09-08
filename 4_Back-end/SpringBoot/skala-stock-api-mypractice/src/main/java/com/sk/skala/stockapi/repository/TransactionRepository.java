package com.sk.skala.stockapi.repository;

import com.sk.skala.stockapi.data.table.Transaction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface TransactionRepository extends JpaRepository<Transaction, Long> {
    
    // 특정 플레이어의 모든 거래 내역 조회 (최신순)
    @Query("SELECT t FROM Transaction t WHERE t.player.playerId = :playerId ORDER BY t.transactionTime DESC")
    List<Transaction> findByPlayerIdOrderByTransactionTimeDesc(@Param("playerId") String playerId);
    
    // 특정 플레이어의 거래 내역을 count 개수만큼 최신순으로 조회
    @Query(value = "SELECT * FROM transaction t WHERE t.player_id = :playerId ORDER BY t.transaction_time DESC LIMIT :count", nativeQuery = true)
    List<Transaction> findByPlayerIdOrderByTransactionTimeDesc(@Param("playerId") String playerId, @Param("count") int count);
    
    // 특정 플레이어의 특정 기간 거래 내역 조회
    @Query("SELECT t FROM Transaction t WHERE t.player.playerId = :playerId " +
           "AND t.transactionTime BETWEEN :startTime AND :endTime " +
           "ORDER BY t.transactionTime DESC")
    List<Transaction> findByPlayerIdAndTimeBetween(@Param("playerId") String playerId,
                                                   @Param("startTime") LocalDateTime startTime,
                                                   @Param("endTime") LocalDateTime endTime);
    
    // 특정 플레이어의 특정 주식에 대한 거래 내역 조회
    @Query("SELECT t FROM Transaction t WHERE t.player.playerId = :playerId " +
           "AND t.stock.id = :stockId ORDER BY t.transactionTime DESC")
    List<Transaction> findByPlayerIdAndStockId(@Param("playerId") String playerId,
                                               @Param("stockId") Long stockId);
    
    // 특정 플레이어의 거래 유형별 조회 (BUY 또는 SELL)
    @Query("SELECT t FROM Transaction t WHERE t.player.playerId = :playerId " +
           "AND t.transactionType = :transactionType ORDER BY t.transactionTime DESC")
    List<Transaction> findByPlayerIdAndTransactionType(@Param("playerId") String playerId,
                                                       @Param("transactionType") String transactionType);
    
    // 특정 플레이어의 거래 내역 개수 조회
    @Query("SELECT COUNT(t) FROM Transaction t WHERE t.player.playerId = :playerId")
    long countByPlayerId(@Param("playerId") String playerId);
    
    // 특정 플레이어의 총 투자금액 계산 (매수만)
    @Query("SELECT COALESCE(SUM(t.totalAmount), 0) FROM Transaction t " +
           "WHERE t.player.playerId = :playerId AND t.transactionType = 'BUY'")
    double getTotalInvestmentByPlayerId(@Param("playerId") String playerId);
    
    // 특정 플레이어의 총 매도금액 계산 (매도만)
    @Query("SELECT COALESCE(SUM(t.totalAmount), 0) FROM Transaction t " +
           "WHERE t.player.playerId = :playerId AND t.transactionType = 'SELL'")
    double getTotalSalesByPlayerId(@Param("playerId") String playerId);
}
