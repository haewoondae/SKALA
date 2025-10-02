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

import com.sk.skala.stockapi.data.common.Response;
import com.sk.skala.stockapi.data.table.Stock;
import com.sk.skala.stockapi.service.StockService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/stocks") // 컨트롤러 기본 URL 경로 지정
@RequiredArgsConstructor
public class StockController {
    
    private final StockService stockService;
    
    /**
     * 전체 주식 목록 조회 API
     * @param offset 시작 위치 (기본값: 0)
     * @param count 조회할 개수 (기본값: 10)
     * @return Response 페이징된 주식 목록
     */
    @GetMapping("/list")
    public Response getAllStocks(
        @RequestParam(defaultValue = "0") int offset,
        @RequestParam(defaultValue = "10") int count
    ) {
        // 서비스에서 페이징 적용된 주식 목록을 받아 반환
        return stockService.getAllStocks(offset, count);
    }
    
    /**
     * 개별 주식 상세 조회 API
     * @param id 주식 ID
     * @return Response 주식 상세 정보
     */
    @GetMapping("/{id}")
    public Response getStockById(@PathVariable Long id) {
        // 서비스에서 해당 주식 정보 반환
        return stockService.getStockById(id);
    }
    
    /**
     * 주식 등록 API
     * @param stock 등록할 주식 정보
     * @return Response 등록된 주식 정보
     */
    @PostMapping
    public Response createStock(@RequestBody Stock stock) {
        // 서비스 통해 새 주식 등록, 결과 반환
        return stockService.createStock(stock);
    }
    
    /**
     * 주식 정보 수정 API
     * @param stock 수정할 주식 정보
     * @return Response 수정된 주식 정보
     */
    @PutMapping
    public Response updateStock(@RequestBody Stock stock) {
        // 서비스 통해 주식 정보 업데이트
        return stockService.updateStock(stock);
    }
    
    /**
     * 주식 삭제 API
     * @param stock 삭제할 주식 정보
     * @return Response 삭제 결과
     */
    @DeleteMapping
    public Response deleteStock(@RequestBody Stock stock) {
        // 서비스로 삭제할 주식 정보 전달
        return stockService.deleteStock(stock);
    }
}