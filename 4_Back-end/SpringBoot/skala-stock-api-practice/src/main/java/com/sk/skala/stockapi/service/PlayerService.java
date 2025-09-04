package com.sk.skala.stockapi.service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.sk.skala.stockapi.data.dto.PlayerStockDto;
import com.sk.skala.stockapi.data.dto.PlayerStockListDto;
import com.sk.skala.stockapi.data.table.Player;
import com.sk.skala.stockapi.data.table.PlayerStock;
import com.sk.skala.stockapi.data.table.Stock;
import com.sk.skala.stockapi.repository.PlayerRepository;
import com.sk.skala.stockapi.repository.PlayerStockRepository;
import com.sk.skala.stockapi.repository.StockRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class PlayerService {
    
    private final StockRepository stockRepository;
    private final PlayerRepository playerRepository;
    private final PlayerStockRepository playerStockRepository;
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
        if (isAnyEmpty(player.getPlayerId(), player.getPlayerPassword())) {
            throw new ParameterException("playerId", "playerPassword");
        }
        
        // 중복 아이디 체크
        Optional<Player> existingPlayer = playerRepository.findById(player.getPlayerId());
        if (existingPlayer.isPresent()) {
            throw new ResponseException(Error.DATA_DUPLICATED);
        }
        
        // Player 객체 생성, 초기자산 세팅 (기본값 1000000.0)
        if (player.getPlayerMoney() == null) {
            player.setPlayerMoney(1000000.0);
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
        if (isAnyEmpty(playerSession.getPlayerId(), playerSession.getPlayerPassword())) {
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
        sessionHandler.storeAccessToken(player.getPlayerId());
        
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
        if (player.getPlayerId() == null || player.getPlayerMoney() == null || player.getPlayerMoney() < 0) {
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
        String playerId = sessionHandler.getCurrentPlayerId();
        
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
            // 기존 보유 주식 수량 추가
            PlayerStock playerStock = existingPlayerStock.get();
            playerStock.setQuantity(playerStock.getQuantity() + order.getQuantity());
            playerStockRepository.save(playerStock);
        } else {
            // 신규 생성
            PlayerStock newPlayerStock = new PlayerStock(player, stock, order.getQuantity());
            playerStockRepository.save(newPlayerStock);
        }
        
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
        String playerId = sessionHandler.getCurrentPlayerId();
        
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
        if (playerStock.getQuantity().equals(order.getQuantity())) {
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
}