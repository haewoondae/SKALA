package com.sk.skala.stockapi.service;

import com.sk.skala.stockapi.data.common.Response;
import com.sk.skala.stockapi.data.dto.WatchlistDto;
import com.sk.skala.stockapi.data.table.Player;
import com.sk.skala.stockapi.data.table.Stock;
import com.sk.skala.stockapi.data.table.Watchlist;
import com.sk.skala.stockapi.repository.PlayerRepository;
import com.sk.skala.stockapi.repository.StockRepository;
import com.sk.skala.stockapi.repository.WatchlistRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class WatchlistService {

    private final WatchlistRepository watchlistRepository;
    private final PlayerRepository playerRepository;
    private final StockRepository stockRepository;

    /**
     * 특정 플레이어의 관심 종목 목록 조회
     */
    public Response getWatchlistByPlayerId(String playerId) {
        try {
            // 플레이어 존재 여부 확인
            Optional<Player> playerOpt = playerRepository.findById(playerId);
            if (playerOpt.isEmpty()) {
                return Response.error("플레이어를 찾을 수 없습니다: " + playerId);
            }

            List<Watchlist> watchlists = watchlistRepository.findByPlayerIdOrderByAddedTimeDesc(playerId);
            
            List<WatchlistDto> watchlistDtos = watchlists.stream()
                    .map(this::convertToDto)
                    .collect(Collectors.toList());

            return Response.success(watchlistDtos);
        } catch (Exception e) {
            return Response.error("관심 종목 목록 조회 중 오류가 발생했습니다: " + e.getMessage());
        }
    }

    /**
     * 관심 종목 추가 (playerId 오버로드)
     */
    @Transactional
    public Response addToWatchlist(String playerId, WatchlistDto watchlistDto) {
        // Builder의 toBuilder() 메서드를 사용하여 playerId만 변경
        return addToWatchlist(watchlistDto.toBuilder().playerId(playerId).build());
    }

    /**
     * 관심 종목 추가
     */
    @Transactional
    public Response addToWatchlist(WatchlistDto watchlistDto) {
        try {
            // 플레이어 존재 여부 확인
            Optional<Player> playerOpt = playerRepository.findById(watchlistDto.getPlayerId());
            if (playerOpt.isEmpty()) {
                return Response.error("플레이어를 찾을 수 없습니다: " + watchlistDto.getPlayerId());
            }

            // 주식 존재 여부 확인
            Optional<Stock> stockOpt = stockRepository.findById(watchlistDto.getStockId());
            if (stockOpt.isEmpty()) {
                return Response.error("주식을 찾을 수 없습니다: " + watchlistDto.getStockId());
            }

            // 이미 관심 종목으로 등록되어 있는지 확인
            boolean exists = watchlistRepository.existsByPlayerIdAndStockId(
                    watchlistDto.getPlayerId(), watchlistDto.getStockId());
            if (exists) {
                return Response.error("이미 관심 종목으로 등록된 주식입니다.");
            }

            // 관심 종목 추가
            Watchlist watchlist = new Watchlist(
                    playerOpt.get(),
                    stockOpt.get(),
                    LocalDateTime.now()
            );

            Watchlist savedWatchlist = watchlistRepository.save(watchlist);
            WatchlistDto resultDto = convertToDto(savedWatchlist);

            return Response.success(resultDto);
        } catch (Exception e) {
            return Response.error("관심 종목 추가 중 오류가 발생했습니다: " + e.getMessage());
        }
    }

    /**
     * 관심 종목 삭제 (ID로)
     */
    @Transactional
    public Response removeFromWatchlist(Long id) {
        try {
            Optional<Watchlist> watchlistOpt = watchlistRepository.findById(id);
            if (watchlistOpt.isEmpty()) {
                return Response.error("관심 종목을 찾을 수 없습니다: " + id);
            }

            watchlistRepository.deleteById(id);
            return Response.success(null);
        } catch (Exception e) {
            return Response.error("관심 종목 삭제 중 오류가 발생했습니다: " + e.getMessage());
        }
    }

    /**
     * 특정 플레이어의 특정 주식 관심 종목 삭제
     */
    @Transactional
    public Response removeFromWatchlistByPlayerAndStock(String playerId, Long stockId) {
        try {
            Optional<Watchlist> watchlistOpt = watchlistRepository.findByPlayerIdAndStockId(playerId, stockId);
            if (watchlistOpt.isEmpty()) {
                return Response.error("해당 관심 종목을 찾을 수 없습니다.");
            }

            watchlistRepository.delete(watchlistOpt.get());
            return Response.success(null);
        } catch (Exception e) {
            return Response.error("관심 종목 삭제 중 오류가 발생했습니다: " + e.getMessage());
        }
    }

    /**
     * 특정 플레이어가 특정 주식을 관심 종목으로 등록했는지 확인
     */
    public Response checkWatchlistExists(String playerId, Long stockId) {
        try {
            boolean exists = watchlistRepository.existsByPlayerIdAndStockId(playerId, stockId);
            return Response.success(exists);
        } catch (Exception e) {
            return Response.error("관심 종목 확인 중 오류가 발생했습니다: " + e.getMessage());
        }
    }

    /**
     * 특정 플레이어의 관심 종목 개수 조회
     */
    public Response getWatchlistCountByPlayerId(String playerId) {
        try {
            // 플레이어 존재 여부 확인
            Optional<Player> playerOpt = playerRepository.findById(playerId);
            if (playerOpt.isEmpty()) {
                return Response.error("플레이어를 찾을 수 없습니다: " + playerId);
            }

            long count = watchlistRepository.countByPlayerId(playerId);
            return Response.success(count);
        } catch (Exception e) {
            return Response.error("관심 종목 개수 조회 중 오류가 발생했습니다: " + e.getMessage());
        }
    }

    /**
     * Watchlist 엔티티를 WatchlistDto로 변환
     */
    private WatchlistDto convertToDto(Watchlist watchlist) {
        return WatchlistDto.builder()
                .id(watchlist.getId())
                .playerId(watchlist.getPlayer().getPlayerId())
                .stockId(watchlist.getStock().getId())
                .stockName(watchlist.getStock().getStockName())
                .currentPrice(watchlist.getStock().getStockPrice())
                .addedTime(watchlist.getAddedTime())
                .build();
    }
}
