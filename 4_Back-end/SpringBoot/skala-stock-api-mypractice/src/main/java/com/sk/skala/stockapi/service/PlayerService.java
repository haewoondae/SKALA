package com.sk.skala.stockapi.service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.sk.skala.stockapi.config.Error;
import com.sk.skala.stockapi.data.common.Response;
import com.sk.skala.stockapi.data.dto.PlayerSession;
import com.sk.skala.stockapi.data.dto.PlayerStockDto;
import com.sk.skala.stockapi.data.dto.PlayerStockListDto;
import com.sk.skala.stockapi.data.dto.StockOrder;
import com.sk.skala.stockapi.data.dto.TransactionDto;
import com.sk.skala.stockapi.data.dto.WatchlistDto;
import com.sk.skala.stockapi.data.table.Player;
import com.sk.skala.stockapi.data.table.PlayerStock;
import com.sk.skala.stockapi.data.table.Stock;
import com.sk.skala.stockapi.data.table.Transaction;
import com.sk.skala.stockapi.data.table.Watchlist;
import com.sk.skala.stockapi.exception.ParameterException;
import com.sk.skala.stockapi.exception.ResponseException;
import com.sk.skala.stockapi.repository.PlayerRepository;
import com.sk.skala.stockapi.repository.PlayerStockRepository;
import com.sk.skala.stockapi.repository.StockRepository;
import com.sk.skala.stockapi.repository.TransactionRepository;
import com.sk.skala.stockapi.repository.WatchlistRepository;
import com.sk.skala.stockapi.tools.StringTool;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class PlayerService {
    
    private final StockRepository stockRepository;
    private final PlayerRepository playerRepository;
    private final PlayerStockRepository playerStockRepository;
    private final TransactionRepository transactionRepository;
    private final WatchlistRepository watchlistRepository;
    private final SessionHandler sessionHandler;
    
    /**
     * 전체 플레이어 목록 조회
     * @param offset 시작 위치
     * @param count 조회할 개수
     * @return Response 페이징된 플레이어 목록
     */
    public Response getAllPlayers(int offset, int count) {
        // Pageable 객체 생성(페이지네이션)
        Pageable pageable = PageRequest.of(offset / count, count);
        
        // playerRepository.findAll(pageable): 페이지 단위 조회
        Page<Player> playerPage = playerRepository.findAll(pageable);
        
        // 결과를 Response로 감싸 반환
        return Response.success(playerPage);
    }
    
    /**
     * 단일 플레이어 및 주식 목록 조회
     * @param playerId 플레이어 ID
     * @return Response 플레이어와 보유 주식 정보
     */
    @Transactional(readOnly = true)
    public Response getPlayerById(String playerId) {
        // playerId로 단일 플레이어 존재 여부 검증
        Optional<Player> playerOptional = playerRepository.findById(playerId);
        if (!playerOptional.isPresent()) {
            throw new ResponseException(Error.DATA_NOT_FOUND, "Player not found");
        }
        
        Player player = playerOptional.get();
        
        // 플레이어가 보유한 PlayerStock 리스트 조회
        List<PlayerStock> playerStocks = playerStockRepository.findByPlayer_PlayerId(playerId);
        
        // Stream API로 DTO 리스트로 변환
        List<PlayerStockDto> stockDtos = playerStocks.stream()
            .map(playerStock -> PlayerStockDto.builder()
                .stockId(playerStock.getStock().getId())
                .stockName(playerStock.getStock().getStockName())
                .stockPrice(playerStock.getStock().getStockPrice())
                .quantity(playerStock.getQuantity())
                .build())
            .collect(Collectors.toList());
        
        // DTO를 Response에 세팅해 반환
        PlayerStockListDto response = PlayerStockListDto.builder()
            .playerId(player.getPlayerId())
            .playerMoney(player.getPlayerMoney())
            .stocks(stockDtos)
            .build();
        
        return Response.success(response);
    }
    
    /**
     * 플레이어 생성
     * @param player 생성할 플레이어 정보
     * @return Response 생성된 플레이어 정보
     */
    public Response createPlayer(Player player) {
        // 입력값 검증
        if (StringTool.isAnyEmpty(player.getPlayerId(), player.getPlayerPassword()) || player.getPlayerMoney() <= 0) {
            throw new ParameterException("playerId", "playerPassword", "playerMoney");
        }
        
        // 중복 아이디 체크
        Optional<Player> existingPlayer = playerRepository.findById(player.getPlayerId());
        if (existingPlayer.isPresent()) {
            throw new ResponseException(Error.DATA_DUPLICATED);
        }
        
        // 저장 후 Response 반환
        Player savedPlayer = playerRepository.save(player);
        return Response.success(savedPlayer);
    }
    
    /**
     * 플레이어 로그인
     * @param playerSession 로그인 세션 정보
     * @return Response 로그인된 플레이어 정보
     */
    public Response loginPlayer(PlayerSession playerSession) {
        // 입력값 검증
        if (StringTool.isAnyEmpty(playerSession.getPlayerId(), playerSession.getPlayerPassword())) {
            throw new ParameterException("playerId", "playerPassword");
        }
        
        // 아이디 검증
        Optional<Player> playerOptional = playerRepository.findById(playerSession.getPlayerId());
        if (!playerOptional.isPresent()) {
            throw new ResponseException(Error.DATA_NOT_FOUND);
        }
        
        Player player = playerOptional.get();
        
        // 패스워드 검증
        if (!player.getPlayerPassword().equals(playerSession.getPlayerPassword())) {
            throw new ResponseException(Error.NOT_AUTHENTICATED);
        }
        
        // 인증 성공 시 sessionHandler.storeAccessToken 호출
        PlayerSession sessionToStore = new PlayerSession();
        sessionToStore.setPlayerId(player.getPlayerId());
        sessionHandler.storeAccessToken(sessionToStore);
        
        // 플레이어 정보 Response의 body에 담아 반환(패스워드 null 처리)
        player.setPlayerPassword(null);
        return Response.success(player);
    }
    
    /**
     * 플레이어 정보 업데이트
     * @param player 업데이트할 플레이어 정보
     * @return Response 업데이트된 플레이어 정보
     */
    public Response updatePlayer(Player player) {
        // playerId, playerMoney 유효성 체크
        if (StringTool.isAnyEmpty(player.getPlayerId()) || player.getPlayerMoney() <= 0) {
            throw new ResponseException(Error.DATA_NOT_FOUND);
        }
        
        // 해당 플레이어 존재 확인
        Optional<Player> existingPlayer = playerRepository.findById(player.getPlayerId());
        if (!existingPlayer.isPresent()) {
            throw new ResponseException(Error.DATA_NOT_FOUND);
        }
        
        // 자산 업데이트
        Player updatedPlayer = existingPlayer.get();
        updatedPlayer.setPlayerMoney(player.getPlayerMoney());
        
        // 저장 후 Response 반환
        Player savedPlayer = playerRepository.save(updatedPlayer);
        return Response.success(savedPlayer);
    }
    
    /**
     * 플레이어 삭제
     * @param player 삭제할 플레이어 정보
     * @return Response 삭제 결과
     */
    public Response deletePlayer(Player player) {
        // playerId로 존재 확인
        Optional<Player> existingPlayer = playerRepository.findById(player.getPlayerId());
        if (!existingPlayer.isPresent()) {
            throw new ResponseException(Error.DATA_NOT_FOUND);
        }
        
        // 삭제 실행
        playerRepository.delete(existingPlayer.get());
        
        // 저장 후 Response 반환
        return Response.success("플레이어가 성공적으로 삭제되었습니다.");
    }
    
    /**
     * 주식 매수
     * @param order 주식 주문 정보
     * @return Response 매수 결과
     */
    @Transactional
    public Response buyPlayerStock(StockOrder order) {
        // 로그인된 playerId 가져오기
        String playerId = sessionHandler.getPlayerId();
        
        // player, stock 엔티티 조회 및 검증
        Optional<Player> playerOptional = playerRepository.findById(playerId);
        Optional<Stock> stockOptional = stockRepository.findById(order.getStockId());
        
        if (!playerOptional.isPresent() || !stockOptional.isPresent()) {
            throw new ResponseException(Error.DATA_NOT_FOUND);
        }
        
        Player player = playerOptional.get();
        Stock stock = stockOptional.get();
        
        // 필요 금액 계산
        double totalCost = stock.getStockPrice() * order.getQuantity();
        
        // 잔액 충분성 체크
        if (player.getPlayerMoney() < totalCost) {
            throw new ResponseException(Error.INSUFFICIENT_FUNDS);
        }
        
        // 잔액 차감
        player.setPlayerMoney(player.getPlayerMoney() - totalCost);
        playerRepository.save(player);
        
        // PlayerStock에 이미 보유한 주식이면 수량 추가, 없으면 신규 생성
        Optional<PlayerStock> existingPlayerStock = playerStockRepository.findByPlayerAndStock(player, stock);
        
        if (existingPlayerStock.isPresent()) {
            // 기존 PlayerStock이 있으면 수량 증가
            PlayerStock playerStock = existingPlayerStock.get();
            playerStock.setQuantity(playerStock.getQuantity() + order.getQuantity());
            playerStockRepository.save(playerStock);
        } else {
            // 기존 PlayerStock이 없으면 새로 생성
            PlayerStock newPlayerStock = new PlayerStock(player, stock, order.getQuantity());
            playerStockRepository.save(newPlayerStock);
        }
        
        // 🔥 추가: 거래 내역 기록 생성
        Transaction transaction = new Transaction(
            player,
            stock,
            "BUY",
            order.getQuantity(),
            stock.getStockPrice(),
            totalCost,
            LocalDateTime.now()
        );
        transactionRepository.save(transaction);
        
        // 요청 처리 결과 Response로 성공 응답
        return Response.success("주식 매수가 완료되었습니다.");
    }
    
    /**
     * 주식 매도
     * @param order 주식 주문 정보
     * @return Response 매도 결과
     */
    @Transactional
    public Response sellPlayerStock(StockOrder order) {
        // 로그인된 playerId 가져오기
        String playerId = sessionHandler.getPlayerId();
        
        // 매도할 Player, Stock 엔티티 조회
        Optional<Player> playerOptional = playerRepository.findById(playerId);
        Optional<Stock> stockOptional = stockRepository.findById(order.getStockId());
        
        if (!playerOptional.isPresent() || !stockOptional.isPresent()) {
            throw new ResponseException(Error.DATA_NOT_FOUND);
        }
        
        Player player = playerOptional.get();
        Stock stock = stockOptional.get();
        
        // PlayerStock 보유수량 검증
        Optional<PlayerStock> playerStockOptional = playerStockRepository.findByPlayerAndStock(player, stock);
        if (!playerStockOptional.isPresent()) {
            throw new ResponseException(Error.DATA_NOT_FOUND);
        }
        
        PlayerStock playerStock = playerStockOptional.get();
        if (playerStock.getQuantity() < order.getQuantity()) {
            throw new ResponseException(Error.INSUFFICIENT_QUANTITY);
        }
        
        // 수량 감소 또는 삭제 처리
        if (playerStock.getQuantity() == order.getQuantity()) {
            // 전량 매도 - 삭제
            playerStockRepository.delete(playerStock);
        } else {
            // 일부 매도 - 수량 감소
            playerStock.setQuantity(playerStock.getQuantity() - order.getQuantity());
            playerStockRepository.save(playerStock);
        }
        
        // 매도 금액만큼 플레이어 자산 증가
        double saleAmount = stock.getStockPrice() * order.getQuantity();
        player.setPlayerMoney(player.getPlayerMoney() + saleAmount);
        playerRepository.save(player);
        
        // 🔥 추가: 거래 내역 기록 생성
        Transaction transaction = new Transaction(
            player,
            stock,
            "SELL",
            order.getQuantity(),
            stock.getStockPrice(),
            saleAmount,
            LocalDateTime.now()
        );
        transactionRepository.save(transaction);
        
        // 요청 처리 결과 Response로 성공 응답
        return Response.success("주식 매도가 완료되었습니다.");
    }
    
    /**
     * 문자열 null/empty 체크 유틸리티 메서드
     */
    private boolean isAnyEmpty(String... values) {
        for (String value : values) {
            if (value == null || value.trim().isEmpty()) {
                return true;
            }
        }
        return false;
    }
    
    // ===== 거래 내역 관련 메서드들 =====
    
    /**
     * 거래 내역을 기록합니다
     * @param player 플레이어 객체
     * @param stock 주식 객체
     * @param transactionType 거래 유형 ("BUY" 또는 "SELL")
     * @param quantity 거래 수량
     * @param price 거래 단가
     */
    @Transactional
    private void recordTransaction(Player player, Stock stock, String transactionType, int quantity, double price) {
        Transaction transaction = new Transaction();
        transaction.setPlayer(player);
        transaction.setStock(stock);
        transaction.setTransactionType(transactionType);
        transaction.setQuantity(quantity);
        transaction.setPrice(price);
        transaction.setTotalAmount(price * quantity);
        transaction.setTransactionTime(LocalDateTime.now());
        
        transactionRepository.save(transaction);
    }
    
    /**
     * 플레이어의 거래 내역을 조회합니다 (최신순으로 제한된 개수)
     * @param playerId 플레이어 ID
     * @param count 조회할 거래 내역 개수 (기본값: 10)
     * @return Response 거래 내역 리스트
     */
    public Response getTransactionHistory(String playerId, int count) {
        try {
            if (StringTool.isAnyEmpty(playerId)) {
                throw new ParameterException("플레이어 ID가 필요합니다.");
            }
            
            if (count <= 0) {
                count = 10; // 기본값
            }
            
            List<Transaction> transactions = transactionRepository.findByPlayerIdOrderByTransactionTimeDesc(playerId);
            
            // count 만큼만 제한
            List<Transaction> limitedTransactions = transactions.stream()
                .limit(count)
                .collect(Collectors.toList());
            
            List<TransactionDto> transactionDtos = limitedTransactions.stream()
                .map(this::convertToTransactionDto)
                .collect(Collectors.toList());
            
            return Response.success(transactionDtos);
            
        } catch (ParameterException e) {
            throw e;
        } catch (Exception e) {
            throw new ResponseException(Error.SYSTEM_ERROR);
        }
    }
    
    /**
     * Transaction 엔티티를 TransactionDto로 변환합니다
     */
    private TransactionDto convertToTransactionDto(Transaction transaction) {
        return TransactionDto.builder()
            .id(transaction.getId())
            .playerId(transaction.getPlayer().getPlayerId())
            .stockId(transaction.getStock().getId())
            .stockName(transaction.getStock().getStockName())
            .transactionType(transaction.getTransactionType())
            .quantity(transaction.getQuantity())
            .price(transaction.getPrice())
            .totalAmount(transaction.getTotalAmount())
            .transactionTime(transaction.getTransactionTime())
            .build();
    }
    
    // ===== 관심 종목 관련 메서드들 =====
    
    /**
     * 관심 종목을 추가합니다
     * @param playerId 플레이어 ID
     * @param stockId 주식 ID
     * @return Response 추가 결과
     */
    @Transactional
    public Response addToWatchlist(String playerId, Long stockId) {
        try {
            if (StringTool.isAnyEmpty(playerId) || stockId == null) {
                throw new ParameterException("플레이어 ID와 주식 ID가 필요합니다.");
            }
            
            // 이미 관심 종목에 있는지 확인
            Optional<Watchlist> existingWatchlist = watchlistRepository.findByPlayerIdAndStockId(playerId, stockId);
            if (existingWatchlist.isPresent()) {
                throw new ParameterException("이미 관심 종목에 추가된 주식입니다.");
            }
            
            // 플레이어와 주식 확인
            Optional<Player> playerOptional = playerRepository.findById(playerId);
            if (!playerOptional.isPresent()) {
                throw new ParameterException("존재하지 않는 플레이어입니다.");
            }
            
            Optional<Stock> stockOptional = stockRepository.findById(stockId);
            if (!stockOptional.isPresent()) {
                throw new ParameterException("존재하지 않는 주식입니다.");
            }
            
            // 관심 종목 추가
            Watchlist watchlist = new Watchlist();
            watchlist.setPlayer(playerOptional.get());
            watchlist.setStock(stockOptional.get());
            watchlist.setAddedTime(LocalDateTime.now());
            
            watchlistRepository.save(watchlist);
            
            return Response.success("관심 종목에 추가되었습니다.");
            
        } catch (ParameterException e) {
            throw e;
        } catch (Exception e) {
            throw new ResponseException(Error.SYSTEM_ERROR);
        }
    }
    
    /**
     * 관심 종목을 제거합니다
     * @param playerId 플레이어 ID
     * @param stockId 주식 ID
     * @return Response 제거 결과
     */
    @Transactional
    public Response removeFromWatchlist(String playerId, Long stockId) {
        try {
            if (StringTool.isAnyEmpty(playerId) || stockId == null) {
                throw new ParameterException("플레이어 ID와 주식 ID가 필요합니다.");
            }
            
            Optional<Watchlist> watchlistOptional = watchlistRepository.findByPlayerIdAndStockId(playerId, stockId);
            if (!watchlistOptional.isPresent()) {
                throw new ParameterException("관심 종목에 없는 주식입니다.");
            }
            
            watchlistRepository.delete(watchlistOptional.get());
            
            return Response.success("관심 종목에서 제거되었습니다.");
            
        } catch (ParameterException e) {
            throw e;
        } catch (Exception e) {
            throw new ResponseException(Error.SYSTEM_ERROR);
        }
    }
    
    /**
     * 플레이어의 관심 종목 목록을 조회합니다
     * @param playerId 플레이어 ID
     * @return Response 관심 종목 리스트
     */
    public Response getWatchlist(String playerId) {
        try {
            if (StringTool.isAnyEmpty(playerId)) {
                throw new ParameterException("플레이어 ID가 필요합니다.");
            }
            
            List<Watchlist> watchlists = watchlistRepository.findByPlayerIdOrderByAddedTimeDesc(playerId);
            
            List<WatchlistDto> watchlistDtos = watchlists.stream()
                .map(this::convertToWatchlistDto)
                .collect(Collectors.toList());
            
            return Response.success(watchlistDtos);
            
        } catch (ParameterException e) {
            throw e;
        } catch (Exception e) {
            throw new ResponseException(Error.SYSTEM_ERROR);
        }
    }
    
    /**
     * Watchlist 엔티티를 WatchlistDto로 변환합니다
     */
    private WatchlistDto convertToWatchlistDto(Watchlist watchlist) {
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