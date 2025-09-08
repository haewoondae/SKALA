package com.sk.skala.stockapi.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.sk.skala.stockapi.data.table.Player;
import com.sk.skala.stockapi.data.table.PlayerStock;
import com.sk.skala.stockapi.data.table.Stock;

public interface PlayerStockRepository extends JpaRepository<PlayerStock, Long> {

    // PlayerStock 엔티티의 player 필드가 참조하는 Player 엔티티의 playerId 필드 값과 일치하는 PlayerStock 목록 조회
    List<PlayerStock> findByPlayer_PlayerId(String playerId);
    
    // 특정 플레이어(Player)가 특정 주식(Stock)을 보유하고 있는지 검색
    Optional<PlayerStock> findByPlayerAndStock(Player player, Stock stock);
}