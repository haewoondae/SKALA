package com.sk.skala.stockapi.service;

import com.sk.skala.stockapi.data.common.Response;
import com.sk.skala.stockapi.data.dto.TransactionDto;
import com.sk.skala.stockapi.data.table.Player;
import com.sk.skala.stockapi.data.table.PlayerStock;
import com.sk.skala.stockapi.data.table.Stock;
import com.sk.skala.stockapi.data.table.Transaction;
import com.sk.skala.stockapi.repository.PlayerRepository;
import com.sk.skala.stockapi.repository.PlayerStockRepository;
import com.sk.skala.stockapi.repository.StockRepository;
import com.sk.skala.stockapi.repository.TransactionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@Transactional(readOnly = true)
public class TransactionService {

    @Autowired
    private TransactionRepository transactionRepository;
    
    @Autowired
    private PlayerRepository playerRepository;
    
    @Autowired
    private StockRepository stockRepository;
    
    @Autowired
    private PlayerStockRepository playerStockRepository;

    /**
     * 특정 플레이어의 매매 기록 조회 (count 개수만큼)
     */
    public Response getTransactionsByPlayerId(String playerId, Integer count) {
        try {
            // 플레이어 존재 여부 확인
            Optional<Player> playerOpt = playerRepository.findById(playerId);
            if (playerOpt.isEmpty()) {
                return Response.error("플레이어를 찾을 수 없습니다: " + playerId);
            }

            List<Transaction> transactions;
            if (count != null && count > 0) {
                // count 개수만큼만 조회
                transactions = transactionRepository.findByPlayerIdOrderByTransactionTimeDesc(playerId, count);
            } else {
                // 전체 조회
                transactions = transactionRepository.findByPlayerIdOrderByTransactionTimeDesc(playerId);
            }

            List<TransactionDto> transactionDtos = transactions.stream()
                    .map(this::convertToDto)
                    .collect(Collectors.toList());

            return Response.success(transactionDtos);
        } catch (Exception e) {
            return Response.error("매매 기록 조회 중 오류가 발생했습니다: " + e.getMessage());
        }
    }

    /**
     * 주식 매수
     */
    @Transactional
    public Response buyStock(TransactionDto transactionDto) {
        try {
            // 입력 유효성 검증
            if (transactionDto.getQuantity() <= 0) {
                return Response.error("매수 수량은 0보다 커야 합니다.");
            }
            if (transactionDto.getPrice() <= 0) {
                return Response.error("매수 가격은 0보다 커야 합니다.");
            }

            // 플레이어 존재 여부 확인
            Optional<Player> playerOpt = playerRepository.findById(transactionDto.getPlayerId());
            if (playerOpt.isEmpty()) {
                return Response.error("플레이어를 찾을 수 없습니다: " + transactionDto.getPlayerId());
            }

            // 주식 존재 여부 확인
            Optional<Stock> stockOpt = stockRepository.findById(transactionDto.getStockId());
            if (stockOpt.isEmpty()) {
                return Response.error("주식을 찾을 수 없습니다: " + transactionDto.getStockId());
            }

            Player player = playerOpt.get();
            Stock stock = stockOpt.get();
            
            // 총 구매 금액 계산
            double totalAmount = transactionDto.getQuantity() * transactionDto.getPrice();
            
            // 플레이어의 잔액 확인
            if (player.getPlayerMoney() < totalAmount) {
                return Response.error("잔액이 부족합니다. 필요 금액: " + totalAmount + ", 현재 잔액: " + player.getPlayerMoney());
            }

            // 거래 기록 생성
            Transaction transaction = new Transaction(
                    player,
                    stock,
                    "BUY",
                    transactionDto.getQuantity(),
                    transactionDto.getPrice(),
                    totalAmount,
                    LocalDateTime.now()
            );
            Transaction savedTransaction = transactionRepository.save(transaction);

            // 플레이어 잔액 차감
            player.setPlayerMoney(player.getPlayerMoney() - totalAmount);
            playerRepository.save(player);

            // 플레이어 보유 주식 업데이트
            updatePlayerStock(player, stock, transactionDto.getQuantity(), true);

            TransactionDto resultDto = convertToDto(savedTransaction);
            return Response.success(resultDto);
        } catch (Exception e) {
            return Response.error("주식 매수 중 오류가 발생했습니다: " + e.getMessage());
        }
    }

    /**
     * 주식 매도
     */
    @Transactional
    public Response sellStock(TransactionDto transactionDto) {
        try {
            // 입력 유효성 검증
            if (transactionDto.getQuantity() <= 0) {
                return Response.error("매도 수량은 0보다 커야 합니다.");
            }
            if (transactionDto.getPrice() <= 0) {
                return Response.error("매도 가격은 0보다 커야 합니다.");
            }

            // 플레이어 존재 여부 확인
            Optional<Player> playerOpt = playerRepository.findById(transactionDto.getPlayerId());
            if (playerOpt.isEmpty()) {
                return Response.error("플레이어를 찾을 수 없습니다: " + transactionDto.getPlayerId());
            }

            // 주식 존재 여부 확인
            Optional<Stock> stockOpt = stockRepository.findById(transactionDto.getStockId());
            if (stockOpt.isEmpty()) {
                return Response.error("주식을 찾을 수 없습니다: " + transactionDto.getStockId());
            }

            Player player = playerOpt.get();
            Stock stock = stockOpt.get();

            // 플레이어가 해당 주식을 보유하고 있는지 확인
            Optional<PlayerStock> playerStockOpt = playerStockRepository.findByPlayerAndStock(player, stock);
            if (playerStockOpt.isEmpty()) {
                return Response.error("해당 주식을 보유하고 있지 않습니다.");
            }

            PlayerStock playerStock = playerStockOpt.get();
            if (playerStock.getQuantity() < transactionDto.getQuantity()) {
                return Response.error("보유 수량이 부족합니다. 보유 수량: " + playerStock.getQuantity() + ", 매도 요청 수량: " + transactionDto.getQuantity());
            }

            // 총 매도 금액 계산
            double totalAmount = transactionDto.getQuantity() * transactionDto.getPrice();

            // 거래 기록 생성
            Transaction transaction = new Transaction(
                    player,
                    stock,
                    "SELL",
                    transactionDto.getQuantity(),
                    transactionDto.getPrice(),
                    totalAmount,
                    LocalDateTime.now()
            );
            Transaction savedTransaction = transactionRepository.save(transaction);

            // 플레이어 잔액 증가
            player.setPlayerMoney(player.getPlayerMoney() + totalAmount);
            playerRepository.save(player);

            // 플레이어 보유 주식 업데이트
            updatePlayerStock(player, stock, transactionDto.getQuantity(), false);

            TransactionDto resultDto = convertToDto(savedTransaction);
            return Response.success(resultDto);
        } catch (Exception e) {
            return Response.error("주식 매도 중 오류가 발생했습니다: " + e.getMessage());
        }
    }

    /**
     * 플레이어 보유 주식 업데이트
     */
    private void updatePlayerStock(Player player, Stock stock, int quantity, boolean isBuy) {
        Optional<PlayerStock> playerStockOpt = playerStockRepository.findByPlayerAndStock(player, stock);
        
        if (isBuy) {
            // 매수인 경우
            if (playerStockOpt.isPresent()) {
                // 기존에 보유하고 있던 주식인 경우 수량 증가
                PlayerStock playerStock = playerStockOpt.get();
                playerStock.setQuantity(playerStock.getQuantity() + quantity);
                playerStockRepository.save(playerStock);
            } else {
                // 새로 구매하는 주식인 경우 새로운 레코드 생성
                PlayerStock newPlayerStock = new PlayerStock(player, stock, quantity);
                playerStockRepository.save(newPlayerStock);
            }
        } else {
            // 매도인 경우
            if (playerStockOpt.isPresent()) {
                PlayerStock playerStock = playerStockOpt.get();
                int newQuantity = playerStock.getQuantity() - quantity;
                
                if (newQuantity > 0) {
                    // 일부 매도인 경우 수량 감소
                    playerStock.setQuantity(newQuantity);
                    playerStockRepository.save(playerStock);
                } else {
                    // 전량 매도인 경우 레코드 삭제
                    playerStockRepository.delete(playerStock);
                }
            }
        }
    }

    /**
     * Transaction 엔티티를 TransactionDto로 변환
     */
    private TransactionDto convertToDto(Transaction transaction) {
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
}
