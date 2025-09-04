package com.sk.skala.stockapi.controller;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.sk.skala.stockapi.data.table.Player;
import com.sk.skala.stockapi.service.PlayerService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/players") // 컨트롤러의 기본 URL 경로로 /api/players 지정
@RequiredArgsConstructor
public class PlayerController {
    
    private final PlayerService playerService;
    
    /**
     * 전체 플레이어 목록 조회 API
     * @param offset 시작 위치 (기본값: 0)
     * @param count 조회할 개수 (기본값: 10)
     * @return Response 페이징된 플레이어 목록
     */
    @GetMapping("/list")
    public Response getAllPlayers(
        @RequestParam(value = "offset", defaultValue = "0") int offset,
        @RequestParam(value = "count", defaultValue = "10") int count
    ) {
        // PlayerService에서 페이징 적용된 플레이어 목록 받아 반환
        return playerService.getAllPlayers(offset, count);
    }
    
    /**
     * 단일 플레이어 상세 조회 API
     * @param playerId 플레이어 ID
     * @return Response 플레이어 상세 정보 + 보유 주식 리스트
     */
    @GetMapping("/{playerId}")
    public Response getPlayerById(@PathVariable String playerId) {
        // 해당 플레이어의 상세 정보 + 보유 주식 리스트 반환
        return playerService.getPlayerById(playerId);
    }
    
    /**
     * 플레이어 등록 API
     * @param player 등록할 플레이어 정보
     * @return Response 등록된 플레이어 정보
     */
    @PostMapping
    public Response createPlayer(@RequestBody Player player) {
        // 서비스로 Player 정보 전달
        // 신규 플레이어 등록 후 Response 반환
        return playerService.createPlayer(player);
    }
    
    /**
     * 플레이어 로그인 API
     * @param playerSession 로그인 세션 정보 (아이디, 비밀번호)
     * @return Response 로그인 결과 및 플레이어 정보
     */
    @PostMapping("/login")
    public Response loginPlayer(@RequestBody PlayerSession playerSession) {
        // 서비스로 PlayerSession(아이디, PW) 전달
        // 로그인 성공 시 토큰/세션 생성 후 플레이어 정보 반환
        return playerService.loginPlayer(playerSession);
    }
    
    /**
     * 플레이어 정보 수정 API
     * @param player 수정할 플레이어 정보
     * @return Response 수정된 플레이어 정보
     */
    @PutMapping
    public Response updatePlayer(@RequestBody Player player) {
        // 서비스로 수정할 플레이어 정보 전달(주로 자산 변경)
        // 플레이어 정보(자산 등) 업데이트
        return playerService.updatePlayer(player);
    }
    
    /**
     * 플레이어 삭제 API
     * @param player 삭제할 플레이어 정보
     * @return Response 삭제 결과
     */
    @DeleteMapping
    public Response deletePlayer(@RequestBody Player player) {
        // 서비스로 삭제할 플레이어 정보 전달(id 필요)
        // 해당 플레이어 삭제
        return playerService.deletePlayer(player);
    }
    
    /**
     * 플레이어 주식 매수 API
     * @param order 주식 주문 정보 (stockId, quantity 등)
     * @return Response 매수 결과
     */
    @PostMapping("/buy")
    public Response buyPlayerStock(@RequestBody StockOrder order) {
        // 서비스로 StockOrder(stockId, quantity 등) 전달
        // 플레이어가 주식 매수
        return playerService.buyPlayerStock(order);
    }
    
    /**
     * 플레이어 주식 매도 API
     * @param order 주식 주문 정보 (stockId, quantity 등)
     * @return Response 매도 결과
     */
    @PostMapping("/sell")
    public Response sellPlayerStock(@RequestBody StockOrder order) {
        // 서비스로 StockOrder 전달
        // 플레이어가 주식 매도
        return playerService.sellPlayerStock(order);
    }
}