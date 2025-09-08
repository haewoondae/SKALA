package com.sk.skala.stockapi.repository;

import com.sk.skala.stockapi.data.table.Watchlist;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface WatchlistRepository extends JpaRepository<Watchlist, Long> {
    
    // 특정 플레이어의 관심 종목 목록 조회 (최신 추가순)
    @Query("SELECT w FROM Watchlist w WHERE w.player.playerId = :playerId ORDER BY w.addedTime DESC")
    List<Watchlist> findByPlayerIdOrderByAddedTimeDesc(@Param("playerId") String playerId);
    
    // 특정 플레이어가 특정 주식을 관심 종목으로 등록했는지 확인
    @Query("SELECT w FROM Watchlist w WHERE w.player.playerId = :playerId AND w.stock.id = :stockId")
    Optional<Watchlist> findByPlayerIdAndStockId(@Param("playerId") String playerId, @Param("stockId") Long stockId);
    
    // 특정 플레이어의 관심 종목 개수 조회
    @Query("SELECT COUNT(w) FROM Watchlist w WHERE w.player.playerId = :playerId")
    long countByPlayerId(@Param("playerId") String playerId);
    
    // 특정 주식을 관심 종목으로 등록한 플레이어 수 조회
    @Query("SELECT COUNT(w) FROM Watchlist w WHERE w.stock.id = :stockId")
    long countByStockId(@Param("stockId") Long stockId);
    
    // 특정 플레이어가 특정 주식을 관심 종목으로 등록했는지 확인 (boolean)
    @Query("SELECT CASE WHEN COUNT(w) > 0 THEN true ELSE false END FROM Watchlist w " +
           "WHERE w.player.playerId = :playerId AND w.stock.id = :stockId")
    boolean existsByPlayerIdAndStockId(@Param("playerId") String playerId, @Param("stockId") Long stockId);
}
