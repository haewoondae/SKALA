package com.sk.skala.stockapi.service;

import java.util.Optional;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import com.sk.skala.stockapi.data.table.Stock;
import com.sk.skala.stockapi.repository.StockRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class StockService {
    
    private final StockRepository stockRepository;
    
    /**
     * 전체 주식 목록 조회 (페이징)
     * @param offset 시작 위치
     * @param count 조회할 개수
     * @return Response 페이징된 주식 목록
     */
    public Response getAllStocks(int offset, int count) {
        // Pageable 객체 생성 (페이징 및 정렬)
        Pageable pageable = PageRequest.of(offset / count, count);
        
        // 데이터 페이지 단위로 조회
        Page<Stock> stockPage = stockRepository.findAll(pageable);
        
        // 결과를 Response 객체에 담아 반환
        return Response.success(stockPage);
    }
    
    /**
     * 개별 주식 상세 조회
     * @param id 주식 ID
     * @return Response 주식 상세 정보
     */
    public Response getStockById(Long id) {
        // ID로 주식 조회, Optional로 존재 여부 확인
        Optional<Stock> stockOptional = stockRepository.findById(id);
        
        // 존재하지 않으면 예외 발생
        if (!stockOptional.isPresent()) {
            throw new ResponseException(Error.DATA_NOT_FOUND);
        }
        
        // 결과를 Response 객체에 담아 반환
        return Response.success(stockOptional.get());
    }
    
    /**
     * 주식 등록(생성)
     * @param stock 등록할 주식 정보
     * @return Response 등록된 주식 정보
     */
    public Response createStock(Stock stock) {
        // 입력값 검증
        if (stock.getStockName() == null || stock.getStockName().trim().isEmpty()) {
            throw new ParameterException("stockName");
        }
        if (stock.getStockPrice() == null || stock.getStockPrice() <= 0) {
            throw new ParameterException("stockPrice");
        }
        
        // 이름 중복 체크
        Optional<Stock> existingStock = stockRepository.findByStockName(stock.getStockName());
        if (existingStock.isPresent()) {
            throw new ResponseException(Error.DATA_DUPLICATED);
        }
        
        // 신규 Stock의 ID는 0L로 설정 (JPA가 자동 생성)
        stock.setId(0L);
        
        // 저장 후 Response 반환
        Stock savedStock = stockRepository.save(stock);
        return Response.success(savedStock);
    }
    
    /**
     * 주식 정보 수정
     * @param stock 수정할 주식 정보
     * @return Response 수정된 주식 정보
     */
    public Response updateStock(Stock stock) {
        // 입력값 검증
        if (stock.getStockName() == null || stock.getStockName().trim().isEmpty()) {
            throw new ParameterException("stockName");
        }
        if (stock.getStockPrice() == null || stock.getStockPrice() <= 0) {
            throw new ParameterException("stockPrice");
        }
        
        // 해당 ID의 Stock이 존재하는지 확인
        Optional<Stock> existingStock = stockRepository.findById(stock.getId());
        if (!existingStock.isPresent()) {
            throw new ResponseException(Error.DATA_NOT_FOUND);
        }
        
        // 수정(덮어쓰기) 후 Response 반환
        Stock updatedStock = stockRepository.save(stock);
        return Response.success(updatedStock);
    }
    
    /**
     * 주식 삭제
     * @param stock 삭제할 주식 정보
     * @return Response 삭제 결과
     */
    public Response deleteStock(Stock stock) {
        // ID로 조회해서 존재하는지 확인
        Optional<Stock> existingStock = stockRepository.findById(stock.getId());
        if (!existingStock.isPresent()) {
            throw new ResponseException(Error.DATA_NOT_FOUND);
        }
        
        // 삭제 실행
        stockRepository.delete(existingStock.get());
        
        // 삭제 후 Response 반환
        return Response.success("주식이 성공적으로 삭제되었습니다.");
    }
}